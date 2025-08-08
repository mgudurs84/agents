#!/usr/bin/env python3
"""
Upload Single Prompt to Vertex AI Prompt Gallery
Simple script to upload one prompt at a time
"""

import os
import sys
import json
import requests
from pathlib import Path
from google.auth import default
from google.auth.transport.requests import Request

# Configuration
PROJECT_ID = "vertex-ai-demo-468112"
LOCATION = "us-central1"

def get_authenticated_session():
    """Get authenticated session for Google Cloud API."""
    try:
        credentials, project = default()
        credentials.refresh(Request())
        
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        })
        
        return session, credentials.token
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None, None

def upload_prompt_to_gallery(prompt_file_path: str, project_id: str = PROJECT_ID) -> bool:
    """
    Upload a single prompt to Vertex AI Prompt Gallery.
    
    Args:
        prompt_file_path (str): Path to the prompt JSON file
        project_id (str): Google Cloud project ID
        
    Returns:
        bool: Success status
    """
    
    print(f"📤 Uploading Prompt to Vertex AI Gallery")
    print(f"=" * 45)
    print(f"File: {prompt_file_path}")
    print(f"Project: {project_id}")
    print()
    
    # Check if file exists
    if not os.path.exists(prompt_file_path):
        print(f"❌ File not found: {prompt_file_path}")
        return False
    
    # Load prompt data
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_data = json.load(f)
        
        prompt_name = prompt_data["name"]
        prompt_content = prompt_data["content"]
        
        print(f"📝 Prompt Details:")
        print(f"   Name: {prompt_name}")
        print(f"   Display Name: {prompt_data['display_name']}")
        print(f"   Content Length: {len(prompt_content)} characters")
        print(f"   Description: {prompt_data['description']}")
        print()
        
    except Exception as e:
        print(f"❌ Failed to load prompt file: {e}")
        return False
    
    # Get authenticated session
    session, token = get_authenticated_session()
    if not session:
        return False
    
    print("✅ Authentication successful")
    
    # Try different API endpoints for Prompt Gallery
    endpoints_to_try = [
        {
            "name": "Prompt Templates API",
            "url": f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{LOCATION}/promptTemplates",
            "method": "POST"
        },
        {
            "name": "Generative AI Prompts API", 
            "url": f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{LOCATION}/prompts",
            "method": "POST"
        },
        {
            "name": "Model Garden Templates API",
            "url": f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{LOCATION}/modelTemplates",
            "method": "POST"
        }
    ]
    
    for attempt, endpoint in enumerate(endpoints_to_try, 1):
        print(f"🔄 Attempt {attempt}: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        
        # Prepare payload
        payload = {
            "name": prompt_name,
            "displayName": prompt_data["display_name"],
            "description": prompt_data["description"],
            "templateText": prompt_content,
            "content": prompt_content,
            "promptText": prompt_content,
            "tags": prompt_data.get("tags", []),
            "version": prompt_data.get("version", "1.0")
        }
        
        try:
            if endpoint["method"] == "POST":
                response = session.post(endpoint["url"], json=payload)
            else:
                response = session.get(endpoint["url"])
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"✅ SUCCESS! Prompt uploaded via {endpoint['name']}")
                print(f"   Response: {response.json()}")
                return True
            
            elif response.status_code == 404:
                print(f"   ⚠️  Endpoint not found - API may not be available")
            
            elif response.status_code == 403:
                print(f"   ❌ Permission denied - check IAM roles")
                print(f"   Required role: Vertex AI Administrator")
            
            else:
                print(f"   ❌ Failed: {response.status_code}")
                try:
                    error_details = response.json()
                    print(f"   Error: {error_details}")
                except:
                    print(f"   Raw response: {response.text[:200]}...")
        
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
        
        print()
    
    # If all API attempts failed, provide manual instructions
    print("🔧 API upload attempts failed - using manual upload instructions:")
    print()
    print("📋 Manual Upload Steps:")
    print("1. Go to: https://console.cloud.google.com/vertex-ai")
    print("2. Look for: Prompt Gallery, Prompt Garden, or Model Garden")
    print("3. Click: Create New Prompt or Create Template")
    print(f"4. Name: {prompt_name}")
    print(f"5. Content: Copy from {prompt_file_path.replace('.json', '.txt')}")
    print("6. Save and Publish")
    
    return False

def list_available_prompts():
    """List available prompt files for upload."""
    print("📁 Available Prompt Files")
    print("=" * 30)
    
    prompts_dir = Path("vertex_prompts")
    
    if not prompts_dir.exists():
        print("❌ vertex_prompts directory not found")
        print("Run 'python create_prompts.py' first")
        return []
    
    json_files = list(prompts_dir.glob("*.json"))
    
    if not json_files:
        print("❌ No prompt JSON files found")
        return []
    
    print(f"Found {len(json_files)} prompt files:")
    for i, file in enumerate(json_files, 1):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
            print(f"  {i}. {file.name}")
            print(f"     Name: {data['name']}")
            print(f"     Length: {len(data['content'])} chars")
        except Exception as e:
            print(f"  {i}. {file.name} (error reading: {e})")
    
    return json_files

def upload_specific_prompt(prompt_choice: str):
    """Upload a specific prompt based on user choice."""
    
    prompts_dir = Path("vertex_prompts")
    
    # Map choices to files
    prompt_files = {
        "1": "csv_json_converter_prompt.json",
        "2": "test_case_generator_prompt.json", 
        "csv": "csv_json_converter_prompt.json",
        "test": "test_case_generator_prompt.json"
    }
    
    if prompt_choice in prompt_files:
        file_path = prompts_dir / prompt_files[prompt_choice]
    else:
        # Try direct filename
        file_path = prompts_dir / prompt_choice
        if not file_path.suffix:
            file_path = prompts_dir / f"{prompt_choice}.json"
    
    if file_path.exists():
        return upload_prompt_to_gallery(str(file_path))
    else:
        print(f"❌ Prompt file not found: {file_path}")
        return False

def main():
    """Main upload function."""
    print("🚀 Upload Prompt to Vertex AI Prompt Gallery")
    print("=" * 50)
    
    # Check credentials
    creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds:
        print("❌ Set credentials first:")
        print('$env:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\key.json"')
        return
    
    print(f"✅ Credentials: {creds}")
    print(f"✅ Project: {PROJECT_ID}")
    print()
    
    # List available prompts
    prompt_files = list_available_prompts()
    
    if not prompt_files:
        return
    
    # Get user choice
    print("\\nWhich prompt would you like to upload?")
    print("1. CSV to JSON Converter Prompt")
    print("2. Test Case Generator Prompt")
    print("Enter choice (1, 2, csv, test, or filename): ", end="")
    
    try:
        choice = input().strip().lower()
        
        if not choice:
            choice = "1"  # Default to CSV converter
        
        print(f"\\nUploading choice: {choice}")
        
        # Upload the selected prompt
        success = upload_specific_prompt(choice)
        
        if success:
            print("\\n🎉 SUCCESS! Prompt uploaded to Vertex AI Prompt Gallery")
            print("\\n📋 Next Steps:")
            print("1. Verify prompt in Google Cloud Console")
            print("2. Test dynamic loading: python test_prompt_loading.py")
            print("3. Deploy agent: python deploy_clean.py")
        else:
            print("\\n⚠️  Automatic upload failed - use manual upload:")
            print("1. Go to: https://console.cloud.google.com/vertex-ai")
            print("2. Find: Prompt Gallery or Model Garden")
            print("3. Create new prompt template")
            print("4. Copy content from vertex_prompts/*.txt files")
        
    except (EOFError, KeyboardInterrupt):
        print("\\nUpload cancelled.")

if __name__ == "__main__":
    main()