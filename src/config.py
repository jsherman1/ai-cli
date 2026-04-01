import json
import os
from pathlib import Path
import typer
import litellm

APP_DIR = Path.home() / ".ai-cli"
CONFIG_FILE = APP_DIR / "config.json"

def configure_cli():
    """Interactive prompt to set up and save API keys and Vertex config."""
    typer.secho("Configuring AI CLI. Press Enter to keep existing keys or skip.", fg=typer.colors.CYAN)
    
    APP_DIR.mkdir(parents=True, exist_ok=True)
    
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

    # Standard API Keys
    config["GEMINI_API_KEY"] = typer.prompt("Gemini API Key (Skip if using Vertex)", default=config.get("GEMINI_API_KEY", ""), hide_input=True)
    config["ANTHROPIC_API_KEY"] = typer.prompt("Anthropic API Key (Skip if using Vertex)", default=config.get("ANTHROPIC_API_KEY", ""), hide_input=True)
    config["OPENAI_API_KEY"] = typer.prompt("OpenAI API Key (Skip if using Vertex)", default=config.get("OPENAI_API_KEY", ""), hide_input=True)
    
    # Vertex AI Configuration
    typer.secho("\n--- Vertex AI Setup (For GCP Hosted Models) ---", fg=typer.colors.CYAN)
    config["VERTEXAI_PROJECT"] = typer.prompt("Vertex AI Project ID", default=config.get("VERTEXAI_PROJECT", "my-vertex-project-id"))
    config["VERTEXAI_LOCATION"] = typer.prompt("Vertex AI Location (e.g., us-east5, us-central1)", default=config.get("VERTEXAI_LOCATION", "us-east5"))

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
        
    typer.secho(f"\n✅ Configuration successfully saved to {CONFIG_FILE}", fg=typer.colors.GREEN)

def load_config_to_env():
    """Injects saved keys and Vertex settings into environment variables for LiteLLM."""
    if not CONFIG_FILE.exists():
        typer.secho("Configuration not found. Please run 'ai-cli configure' first.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        
    # Standard Keys
    if config.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = config["GEMINI_API_KEY"]
    if config.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = config["ANTHROPIC_API_KEY"]
    if config.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
        
    # THE FIX: Explicitly set LiteLLM global properties to override gcloud defaults
    if config.get("VERTEXAI_PROJECT"):
        os.environ["VERTEX_PROJECT"] = config["VERTEXAI_PROJECT"]
        litellm.vertex_project = config["VERTEXAI_PROJECT"]  # Force LiteLLM to use this
        
    if config.get("VERTEXAI_LOCATION"):
        os.environ["VERTEX_LOCATION"] = config["VERTEXAI_LOCATION"]
        litellm.vertex_location = config["VERTEXAI_LOCATION"]  # Force LiteLLM to use this