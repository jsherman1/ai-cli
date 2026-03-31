import typer
from rich.console import Console
from rich.markdown import Markdown

from src.config import configure_cli, load_config_to_env
from src.llm_client import get_llm_response
from src.agents.generator import build_revision_prompt
from src.agents.evaluator import EVALUATOR_SYSTEM_PROMPT, parse_evaluation

app = typer.Typer(help="A multi-agent CLI for arbitrated LLM responses.")
console = Console()

@app.command()
def configure():
    """Set up and save API keys."""
    configure_cli()

@app.command()
def ask(
    prompt: str, 
    model: str = typer.Option("vertex_ai/gemini-2.5-pro", help="The model to query (e.g., vertex_ai/claude-sonnet-4-6)")
):
    """Standard Query: Ask a question and get a single response."""
    load_config_to_env()
    
    try:
        final_text = get_llm_response(model_name=model, prompt=prompt, loading_message=f"Querying {model}...")
        console.print("\n")
        console.print(Markdown(final_text))
        console.print("\n")
    except Exception as e:
        console.print(f"[bold red]Error calling API:[/bold red] {e}")

@app.command()
def arbitrate(
    prompt: str, 
    drafter: str = typer.Option("vertex_ai/gemini-2.5-pro", help="The model to write the draft."),
    reviewer: str = typer.Option("vertex_ai/claude-sonnet-4-6", help="The model to critique the draft."),
    max_rounds: int = typer.Option(3, help="Maximum number of revision loops.")
):
    """Arbitration Loop: Two models debate until consensus is reached."""
    load_config_to_env()
    
    console.print(f"\n[bold green]Starting arbitration for:[/bold green] {prompt}")
    console.print(f"[dim]Drafter: {drafter} | Reviewer: {reviewer}[/dim]\n")
    
    try:
        # Initial Draft
        current_draft = get_llm_response(
            model_name=drafter, 
            prompt=prompt, 
            loading_message=f"{drafter} is writing the initial draft..."
        )
        
        for round_num in range(1, max_rounds + 1):
            console.print(f"[bold blue]--- Round {round_num} ---[/bold blue]")
            
            # Review Phase
            review_prompt = f"Original Request: {prompt}\nCurrent Draft:\n{current_draft}"
            review_response = get_llm_response(
                model_name=reviewer,
                prompt=review_prompt,
                system_prompt=EVALUATOR_SYSTEM_PROMPT,
                loading_message=f"{reviewer} is evaluating the draft..."
            )
            
            is_approved, feedback = parse_evaluation(review_response)
            
            if is_approved:
                console.print("\n[bold green]✅ Consensus Reached![/bold green]\n")
                console.print(Markdown(current_draft))
                return
            
            console.print(f"[bold yellow]⚠️ Revision needed. Reviewer feedback:[/bold yellow]\n{feedback}\n")
            
            # Revision Phase
            update_prompt = build_revision_prompt(prompt, current_draft, feedback)
            current_draft = get_llm_response(
                model_name=drafter,
                prompt=update_prompt,
                loading_message=f"{drafter} is rewriting based on feedback..."
            )
            
        console.print("\n[bold red]❌ Max rounds reached without consensus. Final draft:[/bold red]\n")
        console.print(Markdown(current_draft))

    except Exception as e:
        console.print(f"[bold red]Error during arbitration:[/bold red] {e}")

if __name__ == "__main__":
    app()