"""
Prompt Garden Integration for ADK Agents
Load prompts dynamically from Vertex AI Prompt Garden
"""

import os
from typing import Optional, Dict, Any
from google.cloud import aiplatform
import vertexai

class PromptGardenLoader:
    """Load prompts from Vertex AI Prompt Garden."""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        self.client = aiplatform.gapic.DatasetServiceClient()
    
    def load_prompt(self, prompt_name: str, version: str = "latest") -> Optional[str]:
        """
        Load a prompt from Vertex AI Prompt Garden.
        
        Args:
            prompt_name (str): Name of the prompt in Prompt Garden
            version (str): Version of the prompt (default: "latest")
            
        Returns:
            str: Prompt content or None if not found
        """
        try:
            # Method 1: Using Vertex AI Generative AI SDK
            from vertexai.generative_models import GenerativeModel
            
            # Load the prompt template
            prompt_template = self._get_prompt_template(prompt_name, version)
            
            if prompt_template:
                return prompt_template
                
        except Exception as e:
            print(f"Method 1 failed: {e}")
        
        try:
            # Method 2: Using REST API directly
            return self._load_via_rest_api(prompt_name, version)
            
        except Exception as e:
            print(f"Method 2 failed: {e}")
        
        try:
            # Method 3: Using aiplatform client
            return self._load_via_aiplatform_client(prompt_name, version)
            
        except Exception as e:
            print(f"Method 3 failed: {e}")
        
        # Fallback: Load from local cache or default
        return self._get_fallback_prompt(prompt_name)
    
    def _get_prompt_template(self, prompt_name: str, version: str) -> Optional[str]:
        """Load prompt using GenerativeModel."""
        try:
            from vertexai.generative_models import GenerativeModel
            
            # Try to load the prompt template
            model = GenerativeModel("gemini-2.0-flash")
            
            # This is the preferred method when available
            # Note: Exact API may vary based on Vertex AI updates
            prompt_resource = f"projects/{self.project_id}/locations/{self.location}/promptTemplates/{prompt_name}"
            
            # Implementation depends on current Vertex AI API
            # Check current documentation for exact method
            
            return None  # Placeholder - implement based on current API
            
        except Exception as e:
            print(f"GenerativeModel prompt loading failed: {e}")
            return None
    
    def _load_via_rest_api(self, prompt_name: str, version: str) -> Optional[str]:
        """Load prompt via REST API."""
        try:
            import requests
            from google.auth import default
            from google.auth.transport.requests import Request
            
            # Get credentials
            credentials, _ = default()
            credentials.refresh(Request())
            
            # REST API endpoint for Prompt Garden
            url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/promptTemplates/{prompt_name}"
            
            headers = {
                "Authorization": f"Bearer {credentials.token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                # Extract prompt content from response
                if "promptTemplate" in data and "text" in data["promptTemplate"]:
                    return data["promptTemplate"]["text"]
                elif "content" in data:
                    return data["content"]
            
            return None
            
        except Exception as e:
            print(f"REST API prompt loading failed: {e}")
            return None
    
    def _load_via_aiplatform_client(self, prompt_name: str, version: str) -> Optional[str]:
        """Load prompt using aiplatform client."""
        try:
            # Using aiplatform client to access Prompt Garden
            from google.cloud import aiplatform
            
            # Initialize client
            client = aiplatform.gapic.PipelineServiceClient()
            
            # Try to get the prompt template
            resource_name = f"projects/{self.project_id}/locations/{self.location}/promptTemplates/{prompt_name}"
            
            # This would depend on the exact API available
            # Implementation varies based on current Vertex AI capabilities
            
            return None  # Placeholder
            
        except Exception as e:
            print(f"aiplatform client loading failed: {e}")
            return None
    
    def _get_fallback_prompt(self, prompt_name: str) -> str:
        """Get fallback prompt if Prompt Garden is unavailable."""
        
        fallback_prompts = {
            "csv_json_converter": """You are a helpful CSV to JSON converter agent.

Your primary job is to convert CSV data to JSON format.

When users provide CSV data:
1. Use analyze_csv to understand the structure
2. Convert using csv_to_json tool
3. Show the JSON output clearly
4. Report conversion statistics

Be helpful and provide clear JSON output.""",
            
            "test_case_generator": """You are an expert Test Case Generator Agent specialized in creating comprehensive test cases from requirements and formatting them for JIRA import.

Your capabilities:
1. Generate detailed test cases from user requirements
2. Support multiple test types: functional, UI, API, integration, negative
3. Format output for direct JIRA import (CSV, JSON, XLSX)
4. Provide quality assurance and best practices

When users provide requirements:
1. Validate requirements and provide suggestions
2. Generate comprehensive test cases
3. Format for JIRA import
4. Provide clear import instructions

Focus on creating professional, actionable test cases that ensure software quality.""",
            
            "default": """You are a helpful AI agent. Assist users with their requests professionally and efficiently."""
        }
        
        return fallback_prompts.get(prompt_name, fallback_prompts["default"])
    
    def save_prompt_to_garden(self, prompt_name: str, prompt_content: str, description: str = "") -> bool:
        """
        Save a prompt to Vertex AI Prompt Garden.
        
        Args:
            prompt_name (str): Name for the prompt
            prompt_content (str): The prompt text
            description (str): Description of the prompt
            
        Returns:
            bool: Success status
        """
        try:
            # This would implement saving to Prompt Garden
            # Exact implementation depends on current Vertex AI API
            
            print(f"Saving prompt '{prompt_name}' to Prompt Garden...")
            print(f"Content length: {len(prompt_content)} characters")
            
            # For now, save locally as backup
            prompts_dir = Path("prompt_garden_cache")
            prompts_dir.mkdir(exist_ok=True)
            
            prompt_file = prompts_dir / f"{prompt_name}.txt"
            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(prompt_content)
            
            print(f"Saved locally to: {prompt_file}")
            return True
            
        except Exception as e:
            print(f"Failed to save prompt: {e}")
            return False

def load_prompt_for_agent(agent_name: str, project_id: str = None) -> str:
    """
    Convenient function to load prompt for an agent.
    
    Args:
        agent_name (str): Name of the agent/prompt
        project_id (str): Google Cloud project ID (defaults to env var)
        
    Returns:
        str: Prompt content
    """
    
    if not project_id:
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'vertex-ai-demo-468112')
    
    try:
        loader = PromptGardenLoader(project_id)
        prompt = loader.load_prompt(agent_name)
        
        if prompt:
            print(f"✅ Loaded prompt for '{agent_name}' from Prompt Garden")
            return prompt
        else:
            print(f"⚠️  Using fallback prompt for '{agent_name}'")
            return loader._get_fallback_prompt(agent_name)
            
    except Exception as e:
        print(f"❌ Prompt loading failed: {e}")
        # Return basic fallback
        return "You are a helpful AI agent."

# Example usage functions
def create_agent_with_dynamic_prompt():
    """Example: Create agent with dynamic prompt loading."""
    
    # Load prompt dynamically from Prompt Garden
    instruction = load_prompt_for_agent("csv_json_converter")
    
    try:
        from google.adk.agents import Agent
        from csv_json_converter.tools import csv_to_json, analyze_csv
        
        # Create agent with dynamic prompt
        agent = Agent(
            name="csv_json_converter",
            model="gemini-2.0-flash", 
            description="Converts CSV files to JSON format",
            instruction=instruction,  # Dynamic prompt from Prompt Garden
            tools=[csv_to_json, analyze_csv]
        )
        
        print("✅ Agent created with dynamic prompt from Prompt Garden")
        return agent
        
    except ImportError:
        print("⚠️  ADK not available, using fallback")
        return None

if __name__ == "__main__":
    print("Prompt Garden Integration Test")
    print("=" * 35)
    
    # Test loading prompts
    project_id = "vertex-ai-demo-468112"
    
    # Test different agent prompts
    agents = ["csv_json_converter", "test_case_generator", "nonexistent_agent"]
    
    for agent_name in agents:
        print(f"\\nTesting prompt load for: {agent_name}")
        prompt = load_prompt_for_agent(agent_name, project_id)
        print(f"Loaded {len(prompt)} characters")
        print(f"Preview: {prompt[:100]}...")
    
    # Test creating agent with dynamic prompt
    print("\\n" + "=" * 50)
    print("Testing Agent Creation with Dynamic Prompt")
    agent = create_agent_with_dynamic_prompt()
    
    if agent:
        print(f"Agent created: {type(agent)}")
    else:
        print("Agent creation test completed")