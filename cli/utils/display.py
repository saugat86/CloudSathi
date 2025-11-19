"""Display utilities using Rich for beautiful terminal output."""
import json
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box


console = Console()


def print_error(message: str) -> None:
    """Print error message in red.
    
    Args:
        message: Error message to display
    """
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print success message in green.
    
    Args:
        message: Success message to display
    """
    console.print(f"[bold green]✓[/bold green] {message}")


def print_warning(message: str) -> None:
    """Print warning message in yellow.
    
    Args:
        message: Warning message to display
    """
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")


def print_info(message: str) -> None:
    """Print info message.
    
    Args:
        message: Info message to display
    """
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def display_json(data: Dict[str, Any]) -> None:
    """Display data as formatted JSON.
    
    Args:
        data: Data to display as JSON
    """
    json_str = json.dumps(data, indent=2)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    console.print(syntax)


def display_aws_costs(data: Dict[str, Any]) -> None:
    """Display AWS costs in a formatted table.
    
    Args:
        data: AWS cost data from API
    """
    # Summary panel
    summary = Panel(
        f"[bold]Total Cost:[/bold] ${data.get('total_cost', 0):.2f} {data.get('currency', 'USD')}\n"
        f"[bold]Period:[/bold] {data.get('start_date')} to {data.get('end_date')}",
        title="[bold cyan]AWS Cost Summary[/bold cyan]",
        border_style="cyan"
    )
    console.print(summary)
    
    # Costs by service table
    if data.get('costs_by_service'):
        table = Table(
            title="Costs by Service",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        table.add_column("Service", style="cyan", no_wrap=True)
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Currency", justify="center")
        
        for service in data['costs_by_service']:
            table.add_row(
                service.get('service_name', 'Unknown'),
                f"${service.get('amount', 0):.2f}",
                service.get('currency', 'USD')
            )
        
        console.print(table)
    else:
        print_info("No service-level cost data available")


def display_azure_costs(data: Dict[str, Any]) -> None:
    """Display Azure costs in a formatted table.
    
    Args:
        data: Azure cost data from API
    """
    # Summary panel
    summary = Panel(
        f"[bold]Total Cost:[/bold] ${data.get('total_cost', 0):.2f} {data.get('currency', 'USD')}\n"
        f"[bold]Period:[/bold] {data.get('start_date')} to {data.get('end_date')}",
        title="[bold blue]Azure Cost Summary[/bold blue]",
        border_style="blue"
    )
    console.print(summary)
    
    # Costs by resource group table
    if data.get('costs_by_resource_group'):
        table = Table(
            title="Costs by Resource Group",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        table.add_column("Resource Group", style="cyan", no_wrap=True)
        table.add_column("Amount", justify="right", style="green")
        table.add_column("Currency", justify="center")
        
        for rg in data['costs_by_resource_group']:
            table.add_row(
                rg.get('resource_group', 'Unknown'),
                f"${rg.get('amount', 0):.2f}",
                rg.get('currency', 'USD')
            )
        
        console.print(table)
    else:
        print_info("No resource group cost data available")


def display_recommendation(data: Dict[str, Any]) -> None:
    """Display cost optimization recommendation.
    
    Args:
        data: Recommendation data from API
    """
    recommendation = data.get('recommendation', 'No recommendation available')
    
    panel = Panel(
        f"[bold green]{recommendation}[/bold green]",
        title="[bold yellow]💡 Cost Optimization Recommendation[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(panel)
