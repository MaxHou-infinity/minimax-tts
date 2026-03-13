"""MCP Server for MiniMax TTS — 让 Claude Code / Cursor / Windsurf 等 Agent 调用语音合成。

用法:
  # 直接运行
  python -m minimax_tts.mcp_server

  # 或通过 CLI 入口
  minimax-tts-mcp
"""
import sys
import os

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "MCP SDK 未安装。请运行: pip install 'mcp[cli]'",
        file=sys.stderr,
    )
    sys.exit(1)

from .config import load_config, get_api_key
from .voices import VOICES, LANGUAGES, MODELS

mcp = FastMCP(
    "minimax-tts",
    description="🎙️ MiniMax 语音合成工具 — 支持 100+ 音色、40 种语言",
)


@mcp.tool()
def speak(text: str, voice_id: str = "", speed: float = 0, output_path: str = "") -> str:
    """将文本转为语音并播放。

    Args:
        text: 要合成的文本内容
        voice_id: 音色ID（可选，如 female-shaonv, male-qn-jingying）。留空使用默认音色。
        speed: 语速 0.5-2.0（可选，0 表示使用默认值）
        output_path: 输出文件路径（可选，留空自动生成）
    """
    from .client import MiniMaxTTS

    overrides = {}
    if voice_id:
        overrides["voice_id"] = voice_id
    if speed > 0:
        overrides["speed"] = speed

    try:
        tts = MiniMaxTTS(**overrides)
        path = tts.speak(text, output=output_path or None, play=True)
        return f"✅ 语音合成成功！音频已播放并保存: {path}"
    except Exception as e:
        return f"❌ 语音合成失败: {e}"


@mcp.tool()
def speak_to_file(text: str, output_path: str, voice_id: str = "", speed: float = 0) -> str:
    """将文本转为语音并保存到文件（不播放）。

    Args:
        text: 要合成的文本内容
        output_path: 输出文件路径（如 /tmp/speech.mp3）
        voice_id: 音色ID（可选）
        speed: 语速 0.5-2.0（可选，0 表示使用默认值）
    """
    from .client import MiniMaxTTS

    overrides = {}
    if voice_id:
        overrides["voice_id"] = voice_id
    if speed > 0:
        overrides["speed"] = speed

    try:
        tts = MiniMaxTTS(**overrides)
        path = tts.speak(text, output=output_path, play=False)
        return f"✅ 音频已保存: {path}"
    except Exception as e:
        return f"❌ 语音合成失败: {e}"


@mcp.tool()
def list_voices(language: str = "", gender: str = "") -> str:
    """查看可用的语音音色列表。

    Args:
        language: 按语言筛选（zh=中文, en=英文, ja=日文, ko=韩文, yue=粤语）
        gender: 按性别筛选（male 或 female）
    """
    results = []
    for vid, info in VOICES.items():
        if language and info["lang"] != language:
            continue
        if gender and info["gender"] != gender:
            continue
        g = "♂" if info["gender"] == "male" else "♀" if info["gender"] == "female" else "◎"
        results.append(f"{g} {vid} — {info['name']}: {info['desc']}")

    if not results:
        return "没有匹配的音色。可用语言: zh, en, ja, ko, yue"

    return f"可用音色 ({len(results)} 个):\n" + "\n".join(results)


@mcp.tool()
def list_models() -> str:
    """查看可用的 TTS 模型列表。"""
    lines = ["可用模型:"]
    for mid, desc in MODELS.items():
        lines.append(f"  {mid} — {desc}")
    return "\n".join(lines)


def main():
    """MCP Server 入口。"""
    # 检查 API Key
    try:
        get_api_key()
    except ValueError:
        api_key = os.getenv("MINIMAX_API_KEY", "")
        if not api_key:
            print(
                "⚠️  MINIMAX_API_KEY 未设置。请设置环境变量或运行 minimax-tts config",
                file=sys.stderr,
            )

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
