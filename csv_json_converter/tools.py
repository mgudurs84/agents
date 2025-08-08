"""
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
