"""CloudSathi CLI - Main entry point."""
import typer
from rich.console import Console
from cli.commands import aws, azure, recommend
from cli.utils.config import Config
from cli.utils.api_client import APIClient
from cli.utils.display import print_success, print_error, print_info


app = typer.Typer(
    name="cloudsathi",
    help="CloudSathi - Cloud cost optimization CLI for Nepal's startups",
    add_completion=False
)
console = Console()

# Add command groups
app.add_typer(aws.app, name="aws", help="AWS cost management")
app.add_typer(azure.app, name="azure", help="Azure cost management")

# Add recommend as a direct command
app.command(name="recommend", help="Get cost optimization recommendations")(recommend.recommend)


@app.command()
def version():
    """Show CloudSathi CLI version."""
    from cli import __version__
    console.print(f"[bold cyan]CloudSathi CLI[/bold cyan] version [bold green]{__version__}[/bold green]")


@app.command()
def health(
    api_url: str = typer.Option(
        None,
        "--api-url",
        help="API base URL (overrides config)"
    )
):
    """Check if the CloudSathi API is reachable."""
    config = Config()
    base_url = api_url or config.api_url
    
    print_info(f"Checking API health at {base_url}...")
    
    client = APIClient(base_url)
    if client.health_check():
        print_success(f"API is reachable at {base_url}")
    else:
        print_error(f"Cannot reach API at {base_url}")
        print_info("Make sure the backend server is running:")
        print_info("  cd backend && uvicorn app.main:app --port 8000")
        raise typer.Exit(code=1)


@app.command()
def config(
    key: str = typer.Argument(None, help="Configuration key to get/set"),
    value: str = typer.Argument(None, help="Configuration value to set"),
    show: bool = typer.Option(False, "--show", "-s", help="Show all configuration"),
):
    """Manage CloudSathi CLI configuration."""
    cfg = Config()
    
    if show:
        # Show all configuration
        console.print("[bold cyan]CloudSathi Configuration:[/bold cyan]")
        for k, v in cfg.config.items():
            console.print(f"  [green]{k}[/green]: {v}")
    elif key and value:
        # Set configuration
        cfg.set(key, value)
        print_success(f"Set {key} = {value}")
    elif key:
        # Get configuration
        val = cfg.get(key)
        if val:
            console.print(f"[green]{key}[/green]: {val}")
        else:
            print_error(f"Configuration key '{key}' not found")
    else:
        print_error("Provide a key to get, or key and value to set. Use --show to see all.")
        raise typer.Exit(code=1)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
