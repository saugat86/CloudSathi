# CloudSathi CLI

Command-line interface for CloudSathi - Cloud cost optimization tool for Nepal's startups.

## Installation

```bash
# Install in development mode
pip install -e .

# Or install from requirements
cd backend
pip install -r requirements.txt
```

## Quick Start

```bash
# Check if API is running
cloudsathi health

# Get AWS costs for the last 30 days
cloudsathi aws costs

# Get Azure costs with custom date range
cloudsathi azure costs --start-date 2025-06-01 --end-date 2025-06-19

# Get cost optimization recommendations
cloudsathi recommend --ec2 "high usage" --s3 "moderate usage"

# View help
cloudsathi --help
```

## Commands

### AWS Costs
```bash
cloudsathi aws costs [OPTIONS]

Options:
  --start-date, -s TEXT  Start date (YYYY-MM-DD)
  --end-date, -e TEXT    End date (YYYY-MM-DD)
  --format, -f TEXT      Output format: table or json
  --api-url TEXT         API base URL
```

### Azure Costs
```bash
cloudsathi azure costs [OPTIONS]

Options:
  --start-date, -s TEXT  Start date (YYYY-MM-DD)
  --end-date, -e TEXT    End date (YYYY-MM-DD)
  --format, -f TEXT      Output format: table or json
  --api-url TEXT         API base URL
```

### Recommendations
```bash
cloudsathi recommend [OPTIONS]

Options:
  --cost-data, -d TEXT   Cost data as JSON string or file path
  --ec2 TEXT             EC2 usage description
  --s3 TEXT              S3 usage description
  --rds TEXT             RDS usage description
  --lambda TEXT          Lambda usage description
  --format, -f TEXT      Output format: table or json
  --api-url TEXT         API base URL
```

### Configuration
```bash
# Show all configuration
cloudsathi config --show

# Set API URL
cloudsathi config api_url http://localhost:8000

# Get configuration value
cloudsathi config api_url
```

## Configuration

The CLI stores configuration in `~/.cloudsathi/config.yaml`.

You can also set the API URL via environment variable:
```bash
export CLOUDSATHI_API_URL=http://localhost:8000
```

## Examples

### Get AWS costs with JSON output
```bash
cloudsathi aws costs --start-date 2025-06-01 --end-date 2025-06-19 --format json
```

### Get recommendations from JSON file
```bash
echo '{"EC2": "high usage", "S3": "infrequent access"}' > cost_data.json
cloudsathi recommend --cost-data cost_data.json
```

### Use custom API endpoint
```bash
cloudsathi aws costs --api-url https://api.cloudsathi.com
```

## Requirements

- Python 3.8+
- CloudSathi backend server running
- Network access to the API endpoint

## Documentation

For more information, see the [full documentation](docs/CLI_GUIDE.md).
