# CloudSathi CLI Guide

Complete guide for using the CloudSathi command-line interface.

## Installation

### Quick Install

```bash
cd /path/to/CloudSathi
pip install -e .
```

This installs the `cloudsathi` command globally.

### Verify Installation

```bash
cloudsathi --version
# Output: CloudSathi CLI version 1.0.0
```

## Getting Started

### 1. Start the Backend Server

The CLI requires the CloudSathi backend API to be running:

```bash
cd backend
uvicorn app.main:app --port 8000
```

### 2. Check API Health

```bash
cloudsathi health
```

**Output:**
```
ℹ Checking API health at http://localhost:8000...
✓ API is reachable at http://localhost:8000
```

## Command Reference

### Global Options

```bash
cloudsathi --help    # Show all commands
cloudsathi version   # Show CLI version
cloudsathi health    # Check API connectivity
```

### AWS Cost Commands

#### Get AWS Costs

```bash
cloudsathi aws costs [OPTIONS]
```

**Options:**
- `--start-date, -s TEXT` - Start date (YYYY-MM-DD). Defaults to 30 days ago
- `--end-date, -e TEXT` - End date (YYYY-MM-DD). Defaults to today
- `--format, -f TEXT` - Output format: `table` (default) or `json`
- `--api-url TEXT` - Override API base URL

**Examples:**

```bash
# Get costs for last 30 days (default)
cloudsathi aws costs

# Get costs for specific date range
cloudsathi aws costs --start-date 2025-06-01 --end-date 2025-06-19

# Get costs as JSON
cloudsathi aws costs --start-date 2025-06-01 --end-date 2025-06-19 --format json

# Use custom API endpoint
cloudsathi aws costs --api-url https://api.cloudsathi.com
```

**Sample Output (Table):**

```
┌─────────────────────────────────────────────────────────┐
│                   AWS Cost Summary                      │
├─────────────────────────────────────────────────────────┤
│ Total Cost: $123.45 USD                                 │
│ Period: 2025-06-01 to 2025-06-19                        │
└─────────────────────────────────────────────────────────┘

                    Costs by Service
╭──────────────────────────────┬──────────┬──────────╮
│ Service                      │   Amount │ Currency │
├──────────────────────────────┼──────────┼──────────┤
│ Amazon Elastic Compute Cloud │   $45.67 │ USD      │
│ Amazon Simple Storage Service│   $32.10 │ USD      │
│ Amazon RDS                   │   $45.68 │ USD      │
╰──────────────────────────────┴──────────┴──────────╯
```

### Azure Cost Commands

#### Get Azure Costs

```bash
cloudsathi azure costs [OPTIONS]
```

**Options:** Same as AWS costs command

**Examples:**

```bash
# Get Azure costs for last 30 days
cloudsathi azure costs

# Get costs for specific date range
cloudsathi azure costs --start-date 2025-06-01 --end-date 2025-06-19

# Get costs as JSON
cloudsathi azure costs --format json
```

**Sample Output (Table):**

```
┌─────────────────────────────────────────────────────────┐
│                  Azure Cost Summary                     │
├─────────────────────────────────────────────────────────┤
│ Total Cost: $98.76 USD                                  │
│ Period: 2025-06-01 to 2025-06-19                        │
└─────────────────────────────────────────────────────────┘

                 Costs by Resource Group
╭──────────────────┬──────────┬──────────╮
│ Resource Group   │   Amount │ Currency │
├──────────────────┼──────────┼──────────┤
│ production-rg    │   $45.67 │ USD      │
│ development-rg   │   $32.10 │ USD      │
│ Unassigned       │   $20.99 │ USD      │
╰──────────────────┴──────────┴──────────╯
```

### Recommendation Commands

#### Get Cost Optimization Recommendations

```bash
cloudsathi recommend [OPTIONS]
```

**Options:**
- `--cost-data, -d TEXT` - Cost data as JSON string or file path
- `--ec2 TEXT` - EC2 usage description
- `--s3 TEXT` - S3 usage description
- `--rds TEXT` - RDS usage description
- `--lambda TEXT` - Lambda usage description
- `--format, -f TEXT` - Output format: `table` (default) or `json`
- `--api-url TEXT` - Override API base URL

**Examples:**

```bash
# Using individual service options
cloudsathi recommend --ec2 "high usage" --s3 "moderate usage"

# Using JSON string
cloudsathi recommend --cost-data '{"EC2": "high usage", "S3": "infrequent access"}'

# Using JSON file
echo '{"EC2": "high usage", "S3": "moderate usage"}' > costs.json
cloudsathi recommend --cost-data costs.json

# Get JSON output
cloudsathi recommend --ec2 "high usage" --format json
```

**Sample Output:**

```
┌──────────────────────────────────────────────────────────┐
│       💡 Cost Optimization Recommendation                │
├──────────────────────────────────────────────────────────┤
│ Consider using Reserved Instances for EC2 to reduce      │
│ costs by up to 75%. Move infrequently accessed S3 data   │
│ to Glacier storage class.                                │
└──────────────────────────────────────────────────────────┘
```

### Configuration Commands

#### Manage Configuration

```bash
cloudsathi config [KEY] [VALUE] [OPTIONS]
```

**Options:**
- `--show, -s` - Show all configuration

**Examples:**

```bash
# Show all configuration
cloudsathi config --show

# Set API URL
cloudsathi config api_url http://localhost:8000

# Get configuration value
cloudsathi config api_url

# Set output format preference
cloudsathi config output_format json
```

## Configuration

### Configuration File

The CLI stores configuration in `~/.cloudsathi/config.yaml`:

```yaml
api_url: http://localhost:8000
output_format: table
timeout: 30
```

### Environment Variables

You can override configuration using environment variables:

```bash
export CLOUDSATHI_API_URL=http://localhost:8000
cloudsathi aws costs
```

## Advanced Usage

### Piping and Scripting

```bash
# Save costs to file
cloudsathi aws costs --format json > aws_costs.json

# Process with jq
cloudsathi aws costs --format json | jq '.total_cost'

# Use in scripts
#!/bin/bash
COST=$(cloudsathi aws costs --format json | jq -r '.total_cost')
if (( $(echo "$COST > 100" | bc -l) )); then
    echo "Alert: AWS costs exceed $100!"
fi
```

### Automation

```bash
# Daily cost report
0 9 * * * cloudsathi aws costs --start-date $(date -d '1 day ago' +\%Y-\%m-\%d) --end-date $(date +\%Y-\%m-\%d) | mail -s "Daily AWS Costs" admin@example.com
```

## Troubleshooting

### API Connection Issues

**Problem:** `Error: Failed to connect to API`

**Solutions:**
1. Check if backend server is running:
   ```bash
   curl http://localhost:8000/docs
   ```

2. Verify API URL configuration:
   ```bash
   cloudsathi config api_url
   ```

3. Test connectivity:
   ```bash
   cloudsathi health
   ```

### Date Validation Errors

**Problem:** `Error: end_date must be after start_date`

**Solution:** Ensure start date is before end date:
```bash
cloudsathi aws costs --start-date 2025-06-01 --end-date 2025-06-19
```

### Model Not Loaded

**Problem:** `Error: Recommendation model not loaded`

**Solution:** Train the NLP model first:
```bash
cd nlp/scripts
python train_t5.py
```

Then restart the backend server.

### Authentication Errors

**Problem:** `Error: AWS credentials not configured`

**Solution:** Set up credentials in `.env` file:
```bash
cd backend
cp .env.example .env
# Edit .env with your credentials
```

## Tips and Best Practices

### 1. Use Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias cs='cloudsathi'
alias cs-aws='cloudsathi aws costs'
alias cs-azure='cloudsathi azure costs'

# Usage
cs-aws --start-date 2025-06-01 --end-date 2025-06-19
```

### 2. Default Date Ranges

The CLI defaults to the last 30 days if dates aren't specified:
```bash
cloudsathi aws costs  # Last 30 days
```

### 3. JSON for Automation

Use JSON format for scripting and automation:
```bash
cloudsathi aws costs --format json | jq '.costs_by_service[] | select(.amount > 10)'
```

### 4. Save Configuration

Set your preferred API URL once:
```bash
cloudsathi config api_url http://production-api.cloudsathi.com
```

## Examples

### Monthly Cost Report

```bash
#!/bin/bash
# monthly_report.sh

START_DATE=$(date -d '1 month ago' +%Y-%m-01)
END_DATE=$(date -d '1 month ago' +%Y-%m-%d)

echo "=== Monthly Cloud Cost Report ==="
echo ""
echo "AWS Costs:"
cloudsathi aws costs --start-date $START_DATE --end-date $END_DATE

echo ""
echo "Azure Costs:"
cloudsathi azure costs --start-date $START_DATE --end-date $END_DATE
```

### Cost Comparison

```bash
# Compare this month vs last month
THIS_MONTH=$(cloudsathi aws costs --format json | jq -r '.total_cost')
LAST_MONTH=$(cloudsathi aws costs --start-date $(date -d '1 month ago' +%Y-%m-01) --end-date $(date -d '1 month ago' +%Y-%m-%d) --format json | jq -r '.total_cost')

echo "This month: \$$THIS_MONTH"
echo "Last month: \$$LAST_MONTH"
```

## Support

For issues or questions:
- Check the [Testing Guide](TESTING_GUIDE.md)
- Review the [Test Report](TEST_REPORT.md)
- Open an issue on GitHub

---

**Made with ❤️ in Nepal 🇳🇵**
