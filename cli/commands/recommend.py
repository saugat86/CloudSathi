"""Recommendation commands for CloudSathi CLI."""
import json
import typer
from pathlib import Path
from requests.exceptions import RequestException
from cli.utils.api_client import APIClient
from cli.utils.display import (
    display_recommendation,
    display_json,
    print_error,
    print_info
)
from cli.utils.config import Config


def recommend(
    cost_data: str = typer.Option(
        None,
        "--cost-data",
        "-d",
        help='Cost data as JSON string or file path (e.g., \'{"EC2": "high usage"}\')'
    ),
    ec2: str = typer.Option(None, "--ec2", help="EC2 usage description"),
    s3: str = typer.Option(None, "--s3", help="S3 usage description"),
    rds: str = typer.Option(None, "--rds", help="RDS usage description"),
    lambda_: str = typer.Option(None, "--lambda", help="Lambda usage description"),
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
    """Get cost optimization recommendations based on usage data."""
    # Initialize config
    config = Config()
    
    # Build cost data dictionary
    cost_dict = {}
    
    if cost_data:
        # Check if it's a file path
        if Path(cost_data).exists():
            with open(cost_data, 'r', encoding='utf-8') as f:
                cost_dict = json.load(f)
        else:
            # Parse as JSON string
            try:
                cost_dict = json.loads(cost_data)
            except json.JSONDecodeError as e:
                print_error(f"Invalid JSON: {e}")
                raise typer.Exit(code=1)
    else:
        # Build from individual options
        if ec2:
            cost_dict["EC2"] = ec2
        if s3:
            cost_dict["S3"] = s3
        if rds:
            cost_dict["RDS"] = rds
        if lambda_:
            cost_dict["Lambda"] = lambda_
    
    if not cost_dict:
        print_error("No cost data provided. Use --cost-data or individual service options.")
        raise typer.Exit(code=1)
    
    print_info("Getting cost optimization recommendations...")
    
    # Initialize API client
    base_url = api_url or config.api_url
    client = APIClient(base_url)
    
    try:
        # Get recommendation
        data = client.get_recommendation(cost_dict)
        
        # Display results
        if output_format == "json":
            display_json(data)
        else:
            display_recommendation(data)
            
    except RequestException as e:
        print_error(str(e))
        raise typer.Exit(code=1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise typer.Exit(code=1)
