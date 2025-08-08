# CSV to JSON Agent

A simple Google Vertex AI agent that converts CSV files to JSON format.

## Quick Start

1. Setup credentials:
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\key.json"

2. Run setup:
   python setup_clean.py

3. Deploy:
   python deploy_csv_agent.py

## Usage

Send CSV data:
name,age,city
John,25,NYC
Jane,30,LA

Get JSON output:
[
  {"name": "John", "age": "25", "city": "NYC"},
  {"name": "Jane", "age": "30", "city": "LA"}
]

## Requirements

- Google Cloud Project with Vertex AI enabled
- Service account with Vertex AI Admin role
- Python 3.8+
