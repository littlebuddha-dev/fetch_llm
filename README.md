# 📘 fetch_llm.py User Manual

## Overview
`fetch_llm.py` is a very basic unified CLI interface for interacting with multiple LLM providers (e.g., OpenAI, Ollama, Claude, Gemini, HuggingFace).  
It supports text, image, and audio input, and allows you to choose an interaction mode suited for your task (e.g., chat, reasoning, QA, summary).

## 🔧 Requirements
- Python 3.10+
- Install dependencies:

```bash
pip install aiohttp openai-whisper python-dotenv
brew install ffmpeg  # required for Whisper audio decoding
```

## 🗂 Supported Providers

| Provider     | Description                     | Notes                        |
|--------------|----------------------------------|------------------------------|
| `ollama`     | Local models via Ollama API     | Supports `llava-llama3` for image |
| `openai`     | GPT-3.5 / GPT-4 APIs             | Requires `OPENAI_API_KEY`   |
| `claude`     | Claude 2 / 3                     | API key setup required       |
| `gemini`     | Google Gemini models             | API key setup required       |
| `huggingface`| HuggingFace Inference API        | Model name required          |

## 🚀 Basic Usage

```bash
PYTHONPATH=. python fetch_llm.py <provider> "<your prompt>" [options]
```

Example:

```bash
PYTHONPATH=. python fetch_llm.py openai "What is general relativity?" --mode reasoning
```

## 🎛 CLI Options

| Option               | Description |
|----------------------|-------------|
| `<provider>`         | One of: `ollama`, `openai`, `claude`, `gemini`, `huggingface` |
| `<prompt>`           | Prompt text (optional if using `--input-file` or `--audio`) |
| `--input-file`       | File with one prompt per line |
| `--image`            | Image file (base64-encoded for vision-capable models) |
| `--audio`            | Audio file (WAV, MP3). Transcribed via Whisper |
| `--model`            | Model name |
| `--system`           | Custom system prompt |
| `--mode`             | Purpose mode: `simple`, `chat`, `reasoning`, `qa`, `summary`, `verify` |
| `--json`             | Print full raw JSON response |

## 🎯 Modes

| Mode       | Description                                  |
|------------|----------------------------------------------|
| `simple`   | No system prompt (default)                   |
| `chat`     | Friendly assistant                           |
| `reasoning`| Step-by-step logic explanation               |
| `qa`       | Short factual answers                        |
| `summary`  | Concise summarization                        |
| `verify`   | Comparison, verification, or validation      |

## 🖼️ Image Input Example

```bash
PYTHONPATH=. python fetch_llm.py ollama "Describe this image." --image img.jpg --model llava-llama3
```

## 🎙️ Audio Input Example

```bash
PYTHONPATH=. python fetch_llm.py openai --audio sample.mp3 --mode qa
```

## 🌐 Environment Variables

```bash
export OPENAI_API_KEY=sk-xxxx
```

or via `.env` file:

```env
OPENAI_API_KEY=sk-xxxx
```

## 📦 Project Structure

```
llm_api/
├── fetch_llm.py
├── .env
└── llm_api/
    └── providers/
        ├── base.py
        ├── openai.py
        ├── ollama.py
        ├── claude.py
        ├── gemini.py
        └── huggingface.py
```

## ✅ Example Workflow

```bash
PYTHONPATH=. python fetch_llm.py openai --audio meeting.mp3 --mode summary --json
```
