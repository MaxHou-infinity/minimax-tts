"""MiniMax TTS API client — WebSocket streaming synthesis."""
import json
import struct
import subprocess
import sys
import shutil
from datetime import datetime
from pathlib import Path

try:
    import websockets
    import websockets.sync.client as ws_sync
except ImportError:
    websockets = None

import requests

from .config import load_config, get_api_key


class MiniMaxTTS:
    """MiniMax Text-to-Speech client using WebSocket streaming."""

    WS_URL = "wss://api.minimaxi.com/ws/v1/t2a_v2"
    ASYNC_URL = "https://api.minimaxi.com/v1/t2a_async_v2"
    QUERY_URL = "https://api.minimaxi.com/v1/query/t2a_async_query_v2"
    DOWNLOAD_URL = "https://api.minimaxi.com/v1/files/retrieve_content"

    def __init__(self, api_key: str = None, **overrides):
        self.config = load_config()
        self.config.update({k: v for k, v in overrides.items() if v is not None})
        self.api_key = api_key or get_api_key()

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}

    def _voice_setting(self):
        return {
            "voice_id": self.config["voice_id"],
            "speed": self.config["speed"],
            "vol": self.config["vol"],
            "pitch": self.config["pitch"],
        }

    def _audio_setting(self):
        return {
            "sample_rate": self.config["sample_rate"],
            "bitrate": self.config["bitrate"],
            "format": self.config["format"],
            "channel": 1,
        }

    # ── WebSocket streaming (real-time) ──

    def speak(self, text: str, output: str = None, play: bool = True) -> str:
        """Synthesize text to speech via WebSocket streaming.

        Args:
            text: Text to synthesize.
            output: Optional output file path. Auto-generated if None.
            play: Whether to play audio after synthesis.

        Returns:
            Path to the saved audio file.
        """
        if websockets is None:
            raise ImportError(
                "websockets 未安装。请运行: pip install websockets"
            )

        output_path = self._resolve_output(output)
        audio_chunks = []

        headers = self._headers()

        with ws_sync.connect(self.WS_URL, additional_headers=headers) as ws:
            # 1) task_start
            start_msg = {
                "event": "task_start",
                "model": self.config["model"],
                "voice_setting": self._voice_setting(),
                "audio_setting": self._audio_setting(),
            }
            ws.send(json.dumps(start_msg))

            # 2) send text
            text_msg = {"event": "task_continue", "text": text}
            ws.send(json.dumps(text_msg))

            # 3) signal finish
            finish_msg = {"event": "task_finish"}
            ws.send(json.dumps(finish_msg))

            # 4) receive audio chunks
            while True:
                try:
                    raw = ws.recv(timeout=30)
                except Exception:
                    break

                if isinstance(raw, str):
                    resp = json.loads(raw)
                    # Check for errors
                    if resp.get("base_resp", {}).get("status_code", 0) != 0:
                        err = resp.get("base_resp", {})
                        raise RuntimeError(
                            f"API 错误 [{err.get('status_code')}]: {err.get('status_msg', 'unknown')}"
                        )
                    # Extract audio data
                    audio_hex = resp.get("data", {}).get("audio")
                    if audio_hex:
                        audio_chunks.append(bytes.fromhex(audio_hex))
                    # Check if done
                    if resp.get("data", {}).get("is_final", False):
                        break
                elif isinstance(raw, bytes):
                    audio_chunks.append(raw)

        if not audio_chunks:
            raise RuntimeError("未收到任何音频数据")

        # Save audio
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in audio_chunks:
                f.write(chunk)

        if play:
            self._play_audio(output_path)

        return str(output_path)

    # ── HTTP async synthesis (for long text / file) ──

    def synthesize_async(self, text: str, output: str = None) -> str:
        """Synthesize using the async HTTP API (for longer texts).

        Args:
            text: Text to synthesize.
            output: Optional output path.

        Returns:
            Path to the saved audio file.
        """
        import time

        output_path = self._resolve_output(output)

        # 1) Create task
        payload = {
            "model": self.config["model"],
            "text": text,
            "voice_setting": self._voice_setting(),
            "audio_setting": {
                "audio_sample_rate": self.config["sample_rate"],
                "bitrate": self.config["bitrate"],
                "format": self.config["format"],
                "channel": 1,
            },
        }
        resp = requests.post(
            self.ASYNC_URL,
            headers={**self._headers(), "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        task_id = data.get("task_id")
        if not task_id:
            raise RuntimeError(f"创建任务失败: {data}")

        # 2) Poll for completion
        for _ in range(120):  # max ~10 minutes
            time.sleep(5)
            query_resp = requests.get(
                f"{self.QUERY_URL}?task_id={task_id}",
                headers=self._headers(),
                timeout=30,
            )
            query_data = query_resp.json()
            status = query_data.get("status")
            if status == "Success":
                file_id = query_data.get("file_id")
                break
            elif status == "Failed":
                raise RuntimeError(f"合成失败: {query_data}")
        else:
            raise RuntimeError("合成超时")

        # 3) Download
        dl_resp = requests.get(
            f"{self.DOWNLOAD_URL}?file_id={file_id}",
            headers=self._headers(),
            timeout=60,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(dl_resp.content)

        return str(output_path)

    # ── Helpers ──

    def _resolve_output(self, output: str = None) -> Path:
        if output:
            return Path(output)
        out_dir = Path(self.config["output_dir"])
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return out_dir / f"tts_{ts}.{self.config['format']}"

    @staticmethod
    def _play_audio(path: Path):
        """Play audio file using available system player."""
        path_str = str(path)

        # Try mpv first (cross-platform, best quality)
        if shutil.which("mpv"):
            subprocess.run(
                ["mpv", "--no-terminal", "--really-quiet", path_str],
                check=False,
            )
        # macOS: afplay
        elif sys.platform == "darwin" and shutil.which("afplay"):
            subprocess.run(["afplay", path_str], check=False)
        # Linux: aplay, paplay
        elif shutil.which("paplay"):
            subprocess.run(["paplay", path_str], check=False)
        elif shutil.which("aplay"):
            subprocess.run(["aplay", path_str], check=False)
        # ffplay
        elif shutil.which("ffplay"):
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path_str],
                check=False,
            )
        else:
            # On macOS, `open` as last resort
            if sys.platform == "darwin":
                subprocess.run(["open", path_str], check=False)
            else:
                print(f"⚠️  未找到音频播放器，文件已保存: {path_str}")
                print("   建议安装 mpv: https://mpv.io/installation/")
