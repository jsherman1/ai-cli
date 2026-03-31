# AI-CLI: Multi-Agent LLM Arbitrator

**AI-CLI** is a powerful, cross-platform command-line utility that interacts with various Large Language Models (LLMs) including Gemini, Claude, and OpenAI. Its flagship feature is an **Arbitration Loop**—a multi-agent system where one model drafts a response and another model acts as an expert reviewer, critiquing and forcing revisions until a consensus of high quality is reached.

Built with **Python**, **Typer**, **LiteLLM**, and **Rich**, it provides a beautiful terminal interface and seamless API routing.

---

## Key Features

* **Multi-Provider Support**: Query models from Google AI Studio, Anthropic, OpenAI, and Google Cloud Vertex AI using a single unified interface.
* **The Arbitration Loop**: Pit two models against each other. A drafter generates code or text, and a reviewer critiques it. The loop continues until the reviewer validates the output or the max rounds are hit.
* **Secure Secret Management**: An interactive setup process securely stores API keys and Vertex AI configurations locally without exposing them in shell history.
* **Beautiful Terminal UI**: Live loading spinners and fully rendered Markdown outputs directly in your terminal.

---

## Prerequisites

* **Python 3.9+**
* API Keys for your preferred providers (Google AI Studio, OpenAI, etc.)
* *Optional*: Google Cloud SDK (`gcloud`) authenticated for Vertex AI access.

---

## Installation

It is highly recommended to install this tool within a Python Virtual Environment, especially if your Python installation is managed by Homebrew on macOS.

**1. Clone or navigate to the project directory:**
```bash
cd path/to/ai-cli
```

**2. Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install the package in editable mode:**
```bash
pip install -e .
```

---

## Configuration

Before querying models, initialize your configuration. This interactive prompt will securely save your API keys and Vertex AI settings to `~/.ai-cli/config.json`.

```bash
ai-cli configure
```

> **Vertex AI Users**: When prompted, provide your Google Cloud Project ID and the specific region where your desired models are hosted (e.g., `us-east5` for Claude models). Ensure you have run `gcloud auth application-default login` on your machine.

---

## Usage

### 1. Standard Query (Ask)
Send a direct prompt to a single model and stream the formatted Markdown response.

```bash
ai-cli ask "Explain the concept of quantum entanglement." --model gemini/gemini-2.5-flash
```

### 2. Multi-Agent Arbitration (Arbitrate)
Run a multi-round debate between two models. 

```bash
ai-cli arbitrate "Write a secure Python script to parse a CSV and upload it to a database." \
  --drafter gemini/gemini-3.1-pro \
  --reviewer vertex_ai/claude-sonnet-4-6 \
  --max-rounds 3
```

**How it works:**
1.  **Drafter** creates the initial response.
2.  **Reviewer** evaluates the draft against strict system prompts.
3.  If rejected, the Reviewer's feedback is sent back to the Drafter for a rewrite.
4.  This repeats until the Reviewer outputs `STATUS: APPROVE` or the `--max-rounds` limit is reached.

---

## Supported Model Formats

Because AI-CLI uses **LiteLLM** under the hood, you can access hundreds of models by simply prefixing the provider name.

* **Google AI Studio**: `gemini/gemini-2.5-flash`, `gemini/gemini-3.1-pro`
* **Google Cloud Vertex AI**: `vertex_ai/claude-sonnet-4-6`, `vertex_ai/gemini-3.1-pro`
* **OpenAI**: `openai/gpt-4o`
* **Anthropic (Direct)**: `anthropic/claude-3-5-sonnet-20241022`

For a full list of supported providers and model strings, visit the [LiteLLM Providers Documentation](https://docs.litellm.ai/docs/providers).