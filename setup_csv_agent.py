#!/usr/bin/env python3
"""
Complete Setup Script for CSV to JSON Agent
NO UNICODE CHARACTERS - Windows Compatible
"""

import os
import sys
from pathlib import Path

def create_project_structure():
    """Create the complete project structure."""
    print("Creating Project Structure")
    print("=" * 35)
    
    package_dir = Path("csv_json_converter")
    package_dir.mkdir(exist_ok=True)
    
    print(f"Created package directory: {package_dir}")
    return package_dir

def create_all_files(package_dir):
    """Create all project files."""
    
    # 1. Create __init__.py
    init_content = '''"""
CSV to JSON Agent Package
"""

from .agent import root_agent
from .tools import csv_to_json, analyze_csv
from .prompt import ROOT_AGENT_INSTRUCTION

__version__ = "1.0.0"
__all__ = ["root_agent", "csv_to_json", "analyze_csv", "ROOT_AGENT_INSTRUCTION"]
'''
    
    with open(package_dir / "__init__.py", "w", encoding="utf-8") as f:
        f.write(init_content)
    print("Created __init__.py")
    
    # 2. Create tools.py
    tools_content = '''"""
Tools for the CSV to JSON Agent
"""

import json
import csv
import io
from typing import Dict, Any

def csv_to_json(csv_content: str, output_format: str = "array") -> Dict[str, Any]:
    """Convert CSV content to JSON format."""
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        
        if not rows:
            return {
                "success": False,
                "error": "No data found in CSV",
                "json_output": None,
                "record_count": 0
            }
        
        if output_format == "object":
            json_data = {f"row_{i+1}": row for i, row in enumerate(rows)}
        else:
            json_data = rows
        
        return {
            "success": True,
            "json_output": json_data,
            "json_string": json.dumps(json_data, indent=2),
            "record_count": len(rows),
            "columns": list(rows[0].keys()) if rows else [],
            "format": output_format
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"CSV parsing error: {str(e)}",
            "json_output": None,
            "record_count": 0
        }

def analyze_csv(csv_content: str) -> Dict[str, Any]:
    """Analyze CSV structure and content."""
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        
        if not rows:
            return {"success": False, "error": "No data found in CSV"}
        
        columns = list(rows[0].keys())
        
        return {
            "success": True,
            "total_rows": len(rows),
            "total_columns": len(columns),
            "columns": columns,
            "first_row": rows[0] if rows else None
        }
        
    except Exception as e:
        return {"success": False, "error": f"CSV analysis error: {str(e)}"}
'''
    
    with open(package_dir / "tools.py", "w", encoding="utf-8") as f:
        f.write(tools_content)
    print("Created tools.py")
    
    # 3. Create prompt.py
    prompt_content = '''"""
Prompt for the CSV to JSON Agent
"""

ROOT_AGENT_INSTRUCTION = """You are a helpful CSV to JSON converter agent.

Your primary job is to convert CSV data to JSON format.

When users provide CSV data:
1. Use analyze_csv to understand the structure
2. Convert using csv_to_json tool
3. Show the JSON output clearly
4. Report conversion statistics

Be helpful and provide clear JSON output."""
'''
    
    with open(package_dir / "prompt.py", "w", encoding="utf-8") as f:
        f.write(prompt_content)
    print("Created prompt.py")
    
    # 4. Create agent.py - COMPLETELY CLEAN VERSION
    agent_content = '''"""
CSV to JSON Agent - Simple Implementation
"""

import json
import csv
import io

def csv_to_json_simple(csv_content: str):
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        return {
            "success": True,
            "json_output": rows,
            "json_string": json.dumps(rows, indent=2),
            "record_count": len(rows),
            "columns": list(rows[0].keys()) if rows else []
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def analyze_csv_simple(csv_content: str):
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(csv_reader)
        return {
            "success": True,
            "total_rows": len(rows),
            "columns": list(rows[0].keys()) if rows else []
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

class SimpleCSVAgent:
    """Simple CSV to JSON Agent."""
    
    def __init__(self):
        self.name = "csv_json_converter"
        self.model = "gemini-2.0-flash"
        self.description = "Converts CSV to JSON"
        self.tools = [csv_to_json_simple, analyze_csv_simple]
    
    def __call__(self, query: str) -> str:
        """Process queries."""
        if not query:
            return "Hello! Send me CSV data to convert to JSON!"
        
        # Check if it looks like CSV
        if ',' in query and '\\n' in query:
            analysis = analyze_csv_simple(query)
            if analysis["success"]:
                conversion = csv_to_json_simple(query)
                if conversion["success"]:
                    return f"""CSV to JSON Conversion Complete!

Analysis:
- Rows: {analysis['total_rows']}
- Columns: {', '.join(analysis['columns'])}

JSON Output:
```json
{conversion['json_string']}
```

Successfully converted {conversion['record_count']} records!"""
                else:
                    return f"Conversion failed: {conversion['error']}"
            else:
                return f"Analysis failed: {analysis['error']}"
        
        elif any(word in query.lower() for word in ["hello", "hi", "help"]):
            return """Hello! I'm the CSV to JSON Converter!

How to use:
1. Paste your CSV data directly
2. I'll convert it to JSON format
3. Get clean, formatted results

Example CSV:
name,age,city
John,25,NYC
Jane,30,LA

Just paste your CSV data and I'll handle the rest!"""
        
        else:
            return "Please paste CSV data with column headers and comma-separated values."
    
    def __repr__(self):
        return f"SimpleCSVAgent(name='{self.name}')"

# Try real ADK first, fall back to simple agent
try:
    from google.adk.agents import Agent
    from .prompt import ROOT_AGENT_INSTRUCTION
    from .tools import csv_to_json, analyze_csv
    
    root_agent = Agent(
        name="csv_json_converter",
        model="gemini-2.0-flash",
        description="Converts CSV files to JSON format",
        instruction=ROOT_AGENT_INSTRUCTION,
        tools=[csv_to_json, analyze_csv]
    )
    print("Real ADK Agent created")
    
except ImportError:
    root_agent = SimpleCSVAgent()
    print("Simple Agent created")

if __name__ == "__main__":
    test_csv = """name,age,city
John,25,New York
Jane,30,London
Bob,35,Paris"""
    
    print("Testing CSV to JSON Agent:")
    print("=" * 30)
    
    try:
        response = root_agent(test_csv)
        print(response)
    except Exception as e:
        print(f"Error: {e}")
'''
    
    with open(package_dir / "agent.py", "w", encoding="utf-8") as f:
        f.write(agent_content)
    print("Created agent.py")
    
    return True

def create_deployment_script():
    """Create the deployment script."""
    deploy_content = '''#!/usr/bin/env python3
"""
Simple Deployment Script for CSV to JSON Agent
"""

import os
import sys
import subprocess

PROJECT_ID = "vertex-ai-demo-468112"  # CHANGE THIS
LOCATION = "us-central1"

def main():
    """Deploy the agent."""
    print("CSV to JSON Agent Deployment")
    print("=" * 35)
    
    creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds:
        print("ERROR: Set credentials first:")
        print('$env:GOOGLE_APPLICATION_CREDENTIALS="C:\\\\path\\\\to\\\\key.json"')
        return
    
    print(f"Project: {PROJECT_ID}")
    print(f"Credentials: {creds}")
    
    print("\\nInstalling packages...")
    packages = [
        "google-cloud-aiplatform[adk,agent_engines]",
        "vertexai",
        "google-cloud-storage"
    ]
    
    for pkg in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])
    
    print("Packages installed")
    
    try:
        import vertexai
        from vertexai.preview import reasoning_engines
        from vertexai import agent_engines
        from csv_json_converter import root_agent
        
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=f"gs://{PROJECT_ID}-vertex-ai-staging"
        )
        
        print("\\nDeploying...")
        app = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)
        
        remote_app = agent_engines.create(
            agent_engine=app,
            requirements=["google-cloud-aiplatform[adk,agent_engines]"],
            extra_packages=["./csv_json_converter"]
        )
        
        print("Deployment successful!")
        print(f"Resource: {remote_app.resource_name}")
        
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    main()
'''
    
    with open("deploy_csv_agent.py", "w", encoding="utf-8") as f:
        f.write(deploy_content)
    print("Created deploy_csv_agent.py")

def create_readme():
    """Create README file."""
    readme_content = '''# CSV to JSON Agent

A simple Google Vertex AI agent that converts CSV files to JSON format.

## Quick Start

1. Setup credentials:
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\your\\key.json"

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
'''
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("Created README.md")

def create_test_script():
    """Create a test script."""
    test_content = '''#!/usr/bin/env python3
"""
Test the CSV to JSON Agent locally
"""

def test_agent():
    """Test the agent locally before deployment."""
    print("Testing CSV to JSON Agent")
    print("=" * 30)
    
    try:
        from csv_json_converter import root_agent
        
        test_cases = [
            "Hello!",
            """name,age,city
John,25,New York
Jane,30,London
Bob,35,Paris""",
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\\n--- Test {i} ---")
            print(f"Input: {test[:50]}{'...' if len(test) > 50 else ''}")
            
            try:
                response = root_agent(test)
                print(f"Response: {response[:200]}{'...' if len(response) > 200 else ''}")
                print("SUCCESS")
            except Exception as e:
                print(f"ERROR: {e}")
        
        print("\\nLocal testing complete!")
        
    except ImportError as e:
        print(f"Import failed: {e}")
        print("Run setup_clean.py first")

if __name__ == "__main__":
    test_agent()
'''
    
    with open("test_csv_agent.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    print("Created test_csv_agent.py")

def main():
    """Main setup function."""
    print("CSV to JSON Agent - Complete Setup")
    print("=" * 45)
    print("Creating a simple CSV to JSON converter agent")
    print()
    
    # Create project structure
    package_dir = create_project_structure()
    
    # Create all files
    print("\\nCreating Files...")
    if not create_all_files(package_dir):
        print("File creation failed")
        return
    
    # Create additional scripts
    create_deployment_script()
    create_readme()
    create_test_script()
    
    print("\\nSetup Complete!")
    print("\\nFiles Created:")
    print("   - csv_json_converter/__init__.py")
    print("   - csv_json_converter/agent.py")
    print("   - csv_json_converter/tools.py")
    print("   - csv_json_converter/prompt.py")
    print("   - deploy_csv_agent.py")
    print("   - test_csv_agent.py")
    print("   - README.md")
    
    print("\\nNext Steps:")
    print("1. Test locally:")
    print("   python test_csv_agent.py")
    
    print("\\n2. Setup credentials:")
    print("   - Download service account key from Google Cloud Console")
    print('   - Set: $env:GOOGLE_APPLICATION_CREDENTIALS="C:\\\\path\\\\to\\\\key.json"')
    
    print("\\n3. Deploy:")
    print("   python deploy_csv_agent.py")
    
    print("\\nUsage:")
    print("   Send CSV data like: name,age\\nJohn,25\\nJane,30")
    print('   Get JSON output: [{"name": "John", "age": "25"}, ...]')

if __name__ == "__main__":
    main()