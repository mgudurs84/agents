#!/usr/bin/env python3
"""
Prompt Management Script
Upload and manage prompts in Vertex AI Prompt Garden
"""

import os
import json

def upload_prompt_to_garden(prompt_file_path, project_id="vertex-ai-demo-468112"):
    """Upload a prompt to Vertex AI Prompt Garden."""
    
    print(f"Uploading prompt from: {prompt_file_path}")
    
    try:
        # Load prompt data
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_data = json.load(f)
        
        prompt_name = prompt_data["name"]
        prompt_content = prompt_data["content"]
        
        print(f"Prompt: {prompt_name}")
        print(f"Length: {len(prompt_content)} characters")
        
        # Try to upload to Vertex AI Prompt Garden
        # Note: Implementation depends on current Vertex AI API
        
        # Method 1: Try official API (when available)
        success = _upload_via_api(prompt_data, project_id)
        
        if not success:
            # Method 2: Try REST API
            success = _upload_via_rest(prompt_data, project_id)
        
        if not success:
            # Method 3: Manual instructions
            print("❌ Automatic upload not available")
            print("📝 Manual upload required:")
            print(f"   1. Go to Vertex AI Prompt Garden in Google Cloud Console")
            print(f"   2. Create prompt template named: {prompt_name}")
            print(f"   3. Copy content from: {prompt_file_path}")
            return False
        
        print(f"✅ Successfully uploaded: {prompt_name}")
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

def _upload_via_api(prompt_data, project_id):
    """Upload using official Vertex AI API."""
    try:
        # Placeholder for official API when available
        print("   Trying official Vertex AI Prompt API...")
        return False  # Not yet implemented
    except:
        return False

def _upload_via_rest(prompt_data, project_id):
    """Upload using REST API."""
    try:
        import requests
        from google.auth import default
        from google.auth.transport.requests import Request
        
        credentials, _ = default()
        credentials.refresh(Request())
        
        # REST API endpoint (may vary)
        url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/promptTemplates"
        
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "name": prompt_data["name"],
            "displayName": prompt_data["display_name"],
            "description": prompt_data["description"],
            "content": prompt_data["content"]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            print("   ✅ REST API upload successful")
            return True
        else:
            print(f"   ❌ REST API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   REST API error: {e}")
        return False

def main():
    """Main prompt management function."""
    print("Vertex AI Prompt Garden Management")
    print("=" * 40)
    
    # Check for prompt files
    prompts_dir = Path("vertex_prompts")
    if not prompts_dir.exists():
        print("❌ Prompt files not found")
        print("Run 'python create_prompts.py' first to create prompt templates")
        return
    
    # Find prompt files
    prompt_files = list(prompts_dir.glob("*.json"))
    
    if not prompt_files:
        print("❌ No prompt JSON files found")
        return
    
    print(f"Found {len(prompt_files)} prompt files:")
    for f in prompt_files:
        print(f"   📄 {f}")
    
    # Upload each prompt
    for prompt_file in prompt_files:
        print(f"\n" + "-" * 40)
        upload_prompt_to_garden(prompt_file)
    
    print(f"\n🎉 Prompt management complete!")
    print(f"\nNext steps:")
    print(f"1. Verify prompts in Vertex AI Console")
    print(f"2. Test dynamic loading: python test_prompt_loading.py") 
    print(f"3. Deploy agents: python deploy_csv_agent.py")

if __name__ == "__main__":
    main()
