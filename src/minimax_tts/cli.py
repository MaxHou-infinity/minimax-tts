"""MiniMax TTS CLI — 命令行语音合成工具。"""
import sys
import click

from . import __version__
from .config import load_config, save_config, CONFIG_FILE
from .voices import VOICES, LANGUAGES, MODELS


@click.group()
@click.version_option(__version__, prog_name="minimax-tts")
def main():
    """🎙️  MiniMax TTS — 命令行语音合成工具

    基于 MiniMax 中国区 API，支持 100+ 音色、40 种语言。

    快速开始:

      minimax-tts config           # 配置 API Key

      minimax-tts say "你好世界"   # 语音合成并播放

      minimax-tts voices           # 查看可用音色
    """
    pass


# ── config ──


@main.command()
@click.option("--key", "-k", help="MiniMax API Key（直接设置，不进入交互模式）")
@click.option("--voice", "-v", help="默认音色 ID")
@click.option("--model", "-m", help="默认模型")
@click.option("--speed", type=float, help="语速 (0.5-2.0)")
@click.option("--pitch", type=int, help="音调 (-12 到 12)")
@click.option("--show", is_flag=True, help="仅显示当前配置")
def config(key, voice, model, speed, pitch, show):
    """⚙️  配置 API Key 和默认参数。"""
    cfg = load_config()

    if show:
        _show_config(cfg)
        return

    # Non-interactive mode: apply provided flags
    if any([key, voice, model, speed is not None, pitch is not None]):
        if key:
            cfg["api_key"] = key
        if voice:
            if voice not in VOICES:
                click.echo(f"⚠️  未知音色 '{voice}'，使用 minimax-tts voices 查看可用列表")
                return
            cfg["voice_id"] = voice
        if model:
            if model not in MODELS:
                click.echo(f"⚠️  未知模型 '{model}'，可用: {', '.join(MODELS.keys())}")
                return
            cfg["model"] = model
        if speed is not None:
            cfg["speed"] = max(0.5, min(2.0, speed))
        if pitch is not None:
            cfg["pitch"] = max(-12, min(12, pitch))
        save_config(cfg)
        click.echo("✅ 配置已更新！")
        _show_config(cfg)
        return

    # Interactive mode
    click.echo("🎙️  MiniMax TTS 配置向导\n")

    new_key = click.prompt(
        "API Key (从 platform.minimaxi.com 获取)",
        default=cfg.get("api_key", "") or "",
        show_default=False,
        hide_input=True,
    )
    if new_key:
        cfg["api_key"] = new_key

    click.echo(f"\n当前音色: {cfg['voice_id']} ({VOICES.get(cfg['voice_id'], {}).get('name', '?')})")
    new_voice = click.prompt("默认音色 ID (回车保持)", default=cfg["voice_id"])
    cfg["voice_id"] = new_voice

    click.echo(f"\n当前模型: {cfg['model']}")
    new_model = click.prompt("默认模型 (回车保持)", default=cfg["model"])
    cfg["model"] = new_model

    save_config(cfg)
    click.echo(f"\n✅ 配置已保存到 {CONFIG_FILE}")
    _show_config(cfg)


def _show_config(cfg):
    """Display current configuration."""
    key_display = cfg["api_key"][:8] + "..." if cfg.get("api_key") else "(未设置)"
    voice_info = VOICES.get(cfg["voice_id"], {})
    voice_name = voice_info.get("name", "未知")

    click.echo(f"""
┌─────────────────────────────────────┐
│  MiniMax TTS 当前配置               │
├─────────────────────────────────────┤
│  API Key:   {key_display:<24s}│
│  模型:      {cfg['model']:<24s}│
│  音色:      {cfg['voice_id']:<24s}│
│  音色名:    {voice_name:<24s}│
│  语速:      {str(cfg['speed']):<24s}│
│  音调:      {str(cfg['pitch']):<24s}│
│  格式:      {cfg['format']:<24s}│
│  输出目录:  ~/.minimax-tts/audio    │
└─────────────────────────────────────┘""")


# ── say ──


@main.command()
@click.argument("text", required=False)
@click.option("--voice", "-v", help="音色 ID（覆盖默认）")
@click.option("--model", "-m", help="模型（覆盖默认）")
@click.option("--speed", "-s", type=float, help="语速 (0.5-2.0)")
@click.option("--pitch", "-p", type=int, help="音调 (-12 到 12)")
@click.option("--output", "-o", help="输出文件路径")
@click.option("--no-play", is_flag=True, help="仅保存，不播放")
@click.option("--async-mode", is_flag=True, help="使用异步接口（适合长文本）")
def say(text, voice, model, speed, pitch, output, no_play, async_mode):
    """🗣️  语音合成 — 将文本转为语音。

    直接传入文本:

      minimax-tts say "你好，我是 Mini"

    从标准输入读取（适合管道）:

      echo "你好世界" | minimax-tts say

      cat article.txt | minimax-tts say --no-play -o speech.mp3
    """
    from .client import MiniMaxTTS

    # Read from stdin if no text argument
    if not text:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            click.echo("请输入文本（Ctrl+D 结束）:")
            text = sys.stdin.read().strip()

    if not text:
        click.echo("❌ 没有输入文本")
        return

    overrides = {}
    if voice:
        overrides["voice_id"] = voice
    if model:
        overrides["model"] = model
    if speed is not None:
        overrides["speed"] = speed
    if pitch is not None:
        overrides["pitch"] = pitch

    try:
        tts = MiniMaxTTS(**overrides)
        click.echo(f"🎙️  正在合成... ({len(text)} 字)")

        if async_mode:
            path = tts.synthesize_async(text, output=output)
        else:
            path = tts.speak(text, output=output, play=not no_play)

        click.echo(f"✅ 音频已保存: {path}")
    except Exception as e:
        click.echo(f"❌ 合成失败: {e}", err=True)
        sys.exit(1)


# ── voices ──


@main.command()
@click.option("--lang", "-l", help="按语言筛选 (zh/en/ja/ko/yue)")
@click.option("--gender", "-g", type=click.Choice(["male", "female"]), help="按性别筛选")
@click.option("--search", "-s", help="搜索音色名称或描述")
def voices(lang, gender, search):
    """🎭 查看可用音色列表。

    查看全部:     minimax-tts voices

    只看中文女声:  minimax-tts voices -l zh -g female

    搜索:         minimax-tts voices -s 少女
    """
    filtered = {}
    for vid, info in VOICES.items():
        if lang and info["lang"] != lang:
            continue
        if gender and info["gender"] != gender:
            continue
        if search and search.lower() not in (
            vid + info["name"] + info["desc"]
        ).lower():
            continue
        filtered[vid] = info

    if not filtered:
        click.echo("没有匹配的音色。")
        return

    # Group by language
    by_lang = {}
    for vid, info in filtered.items():
        lang_key = info["lang"]
        by_lang.setdefault(lang_key, []).append((vid, info))

    for lang_key, items in by_lang.items():
        lang_name = LANGUAGES.get(lang_key, lang_key)
        click.echo(f"\n{'─' * 50}")
        click.echo(f"  {lang_name}")
        click.echo(f"{'─' * 50}")
        for vid, info in items:
            gender_icon = "♂" if info["gender"] == "male" else "♀" if info["gender"] == "female" else "◎"
            click.echo(f"  {gender_icon} {vid:<35s} {info['name']}")
            click.echo(f"    {info['desc']}")

    click.echo(f"\n共 {len(filtered)} 个音色")
    click.echo("使用方法: minimax-tts say -v <voice_id> \"你好\"")


# ── models ──


@main.command()
def models():
    """📋 查看可用模型列表。"""
    click.echo("\n可用模型:")
    click.echo("─" * 50)
    for mid, desc in MODELS.items():
        click.echo(f"  {mid:<22s} {desc}")
    click.echo()
    click.echo("设置默认: minimax-tts config --model speech-2.8-hd")


# ── test ──


@main.command()
def test():
    """🧪 测试 API 连接和音色效果。"""
    from .client import MiniMaxTTS

    cfg = load_config()
    if not cfg.get("api_key"):
        click.echo("❌ 请先配置 API Key: minimax-tts config")
        return

    click.echo("🧪 测试 MiniMax TTS 连接...\n")
    click.echo(f"  模型: {cfg['model']}")
    click.echo(f"  音色: {cfg['voice_id']}")

    try:
        tts = MiniMaxTTS()
        path = tts.speak("你好，我是你的 AI 语音助手，很高兴认识你！", play=True)
        click.echo(f"\n✅ 测试成功！音频: {path}")
    except Exception as e:
        click.echo(f"\n❌ 测试失败: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
