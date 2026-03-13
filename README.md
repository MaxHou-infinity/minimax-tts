# 🎙️ MiniMax TTS CLI

> **给 Agent 的一键安装（复制这段发给你的 AI Agent）：**

```bash
# 安装
pip install git+https://github.com/MaxHou-infinity/minimax-tts.git

# 配置 API Key（把 "你的API_KEY" 换成你的 MiniMax API Key）
minimax-tts config --key "你的API_KEY"

# 使用
minimax-tts say "你好，我是你的 AI 助手"
```

---

## 详细介绍

命令行语音合成工具，基于 [MiniMax 中国区 API](https://platform.minimaxi.com/)。

支持 **100+ 系统音色**、**40 种语言**，一行命令将文本变成语音。

## 安装

```bash
pip install minimax-tts
```

## 快速开始

### 1. 配置 API Key

前往 [MiniMax 开放平台](https://platform.minimaxi.com/) 获取 API Key（API 或 Coding Plan），然后：

```bash
minimax-tts config
```

或直接设置：

```bash
minimax-tts config --key "你的API_KEY"
```

也支持环境变量：

```bash
export MINIMAX_API_KEY="你的API_KEY"
```

### 2. 语音合成

```bash
# 直接说话
minimax-tts say "你好，我是你的 AI 助手"

# 指定音色
minimax-tts say -v male-qn-jingying "今天天气真不错"

# 调整语速和音调
minimax-tts say -s 1.2 -p 2 "快一点说话"

# 只保存不播放
minimax-tts say --no-play -o output.mp3 "保存到文件"

# 管道模式（适合 Agent 调用）
echo "从管道输入" | minimax-tts say
cat article.txt | minimax-tts say --no-play -o speech.mp3
```

### 3. 查看音色

```bash
# 全部音色
minimax-tts voices

# 只看中文女声
minimax-tts voices -l zh -g female

# 搜索
minimax-tts voices -s 少女
```

### 4. 测试连接

```bash
minimax-tts test
```

## 命令一览

| 命令 | 说明 |
|------|------|
| `minimax-tts config` | 配置 API Key 和默认参数 |
| `minimax-tts say TEXT` | 语音合成并播放 |
| `minimax-tts voices` | 查看可用音色（100+） |
| `minimax-tts models` | 查看可用模型 |
| `minimax-tts test` | 测试 API 连接 |

## 可用模型

| 模型 | 特点 |
|------|------|
| `speech-2.8-hd` | 精准音调还原，高相似度（推荐） |
| `speech-2.6-hd` | 超低延迟，高自然度 |
| `speech-2.8-turbo` | 精准音调，更快更省 |
| `speech-2.6-turbo` | 速度优先，适合语音聊天 |
| `speech-02-hd` | 优秀节奏感，高稳定性 |
| `speech-02-turbo` | 强节奏感，增强多语言支持 |

## 音色示例

**中文音色：** 少女、御姐、甜美女声、青涩青年、精英青年、霸道青年、大学生、病娇弟弟、俊朗男友、霸道少爷、傲娇大小姐...

**英文音色：** Trustworthy Man、Graceful Lady、Whispering Girl、Aussie Bloke...

**日文/韩文/粤语** 等更多音色运行 `minimax-tts voices` 查看。

## 🤖 Agent 集成指南

### 方式 1：CLI 命令行（所有 Agent 通用）

几乎所有 AI Agent 都能执行终端命令，这是最简单的集成方式：

```bash
# Agent 执行这条命令就能"说话"
minimax-tts say "你好，我是你的 AI 助手"

# 管道模式 — Agent 把回答通过管道传入
echo "Agent 的回答内容" | minimax-tts say
```

**适用：** Hermes Agent、Claude Code、Codex、OpenClaw、任何能跑终端的 Agent

只需在 Agent 的系统提示里加一句：
> "你可以通过执行 `minimax-tts say "文本"` 来朗读回复"

### 方式 2：MCP Server（Claude Code / Cursor / Windsurf）

MCP 是 AI Agent 的标准工具协议。安装后 Agent 自动发现语音工具：

```bash
# 安装（含 MCP 依赖）
pip install "minimax-tts[mcp] @ git+https://github.com/MaxHou-infinity/minimax-tts.git"
```

**Claude Code 配置** (`~/.claude.json`)：
```json
{
  "mcpServers": {
    "minimax-tts": {
      "command": "minimax-tts-mcp",
      "env": { "MINIMAX_API_KEY": "你的API_KEY" }
    }
  }
}
```

**Cursor 配置** (`.cursor/mcp.json`)：
```json
{
  "mcpServers": {
    "minimax-tts": {
      "command": "minimax-tts-mcp",
      "env": { "MINIMAX_API_KEY": "你的API_KEY" }
    }
  }
}
```

配置后，Agent 自动获得以下工具：
- `speak` — 合成语音并播放
- `speak_to_file` — 合成语音保存到文件
- `list_voices` — 查看可用音色
- `list_models` — 查看可用模型

### 方式 3：Hermes Agent 原生集成

MiniMax 已作为 Hermes Agent 的第 4 个 TTS provider 内置。配置 `~/.hermes/config.yaml`：

```yaml
tts:
  provider: minimax
  minimax:
    voice_id: female-shaonv    # 音色
    model: speech-2.8-hd       # 模型
    speed: 1.0                 # 语速
```

然后设置环境变量：
```bash
echo 'MINIMAX_API_KEY=你的KEY' >> ~/.hermes/.env
```

Hermes Agent 的 `text_to_speech` 工具会自动使用 MiniMax。

### 方式 4：Python 库直接调用

```python
from minimax_tts.client import MiniMaxTTS

tts = MiniMaxTTS(
    api_key="your-key",
    voice_id="female-shaonv",
    speed=1.0,
)

# 合成并播放
tts.speak("你好，我是 Mini，你的 AI 助手！")

# 只保存不播放
path = tts.speak("保存到文件", play=False)
```

## 配置文件

配置保存在 `~/.minimax-tts/config.json`，音频保存在 `~/.minimax-tts/audio/`。

## 播放器

优先使用 [mpv](https://mpv.io/installation/)，也支持 macOS `afplay`、Linux `paplay/aplay`、`ffplay`。

## License

MIT
