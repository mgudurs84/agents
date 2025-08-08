"""
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
        if ',' in query and '\n' in query:
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
