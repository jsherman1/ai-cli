from litellm import completion
from rich.console import Console

console = Console()

def get_llm_response(model_name: str, prompt: str, system_prompt: str = None, loading_message: str = "Thinking...") -> str:
    """Calls the LLM with an optional system prompt and a loading spinner."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
        
    messages.append({"role": "user", "content": prompt})

    with console.status(f"[bold cyan]{loading_message}[/bold cyan]", spinner="dots"):
        response = completion(
            model=model_name, 
            messages=messages,
            stream=False 
        )
        
    return response.choices[0].message.content