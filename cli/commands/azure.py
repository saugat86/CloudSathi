"""Azure cost commands for CloudSathi CLI."""
from datetime import date, timedelta
import typer
from requests.exceptions import RequestException
from cli.utils.api_client import APIClient
from cli.utils.display import (
    display_azure_costs,
    display_json,
    print_error,
    print_info
)
from cli.utils.config import Config


app = typer.Typer(help="Azure cost management commands")
config = Config()


@app.command("costs")
def get_costs(
    start_date: str = typer.Option(
        None,
        "--start-date",
        "-s",
        help="Start date (YYYY-MM-DD). Defaults to 30 days ago."
    ),
    end_date: str = typer.Option(
        None,
        "--end-date",
        "-e",
        help="End date (YYYY-MM-DD). Defaults to today."
    ),
    output_format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format: table or json"
    ),
    api_url: str = typer.Option(
        None,
        "--api-url",
        help="API base URL (overrides config)"
    )
):
    """Get Azure cost and usage data."""
    # Set default dates if not provided
    if not end_date:
        end_date = date.today().isoformat()
    if not start_date:
        start_date = (date.today() - timedelta(days=30)).isoformat()
    
    print_info(f"Fetching Azure costs from {start_date} to {end_date}...")
    
    # Initialize API client
    base_url = api_url or config.api_url
    client = APIClient(base_url)
    
    try:
        # Fetch costs
        data = client.get_azure_costs(start_date, end_date)
        
        # Display results
        if output_format == "json":
            display_json(data)
        else:
            display_azure_costs(data)
            
    except RequestException as e:
        print_error(str(e))
        raise typer.Exit(code=1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)
