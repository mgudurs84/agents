#!/usr/bin/env python3
"""
Working Script to Upload Prompts to Vertex AI Prompt Management
Uses official Vertex AI SDK with vertexai.preview.prompts module
"""

import os
import json
import sys
from pathlib import Path

# Configuration
PROJECT_ID = "vertex-ai-demo-468112"  # Change to your project ID
LOCATION = "us-central1"

def setup_vertex_ai():
    """Initialize Vertex AI."""
    try:
        import vertexai
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print(f"✅ Vertex AI initialized")
        print(f"   Project: {PROJECT_ID}")
        print(f"   Location: {LOCATION}")
        return True
    except Exception as e:
        print(f"❌ Vertex AI initialization failed: {e}")
        return False

def create_and_save_prompt(prompt_name: str, prompt_content: str, description: str = "") -> bool:
    """
    Create and save a prompt to Vertex AI Prompt Management.
    
    Args:
        prompt_name (str): Name for the prompt
        prompt_content (str): The prompt text content
        description (str): Description of the prompt
        
    Returns:
        bool: Success status
    """
    
    print(f"📤 Creating Prompt in Vertex AI")
    print(f"=" * 35)
    print(f"Name: {prompt_name}")
    print(f"Content length: {len(prompt_content)} characters")
    print(f"Description: {description}")
    print()
    
    try:
        # Import the official Vertex AI prompt management modules
        import vertexai
        from vertexai.preview import prompts
        from vertexai.preview.prompts import Prompt
        
        print("✅ Imported Vertex AI prompt modules")
        
        # Create a local Prompt object
        print("📝 Creating Prompt object...")
        
        local_prompt = Prompt(
            prompt_name=prompt_name,
            prompt_data=prompt_content,
            model_name="gemini-2.0-flash-001",
            system_instruction=description if description else f"This is the {prompt_name} prompt template"
        )
        
        print("✅ Prompt object created successfully")
        
        # Save Prompt to Vertex AI online resource
        print("💾 Saving to Vertex AI Prompt Management...")
        
        # This creates a version and saves it to Vertex AI
        saved_prompt = prompts.create_version(prompt=local_prompt)
        
        print("✅ SUCCESS! Prompt saved to Vertex AI")
        print(f"📋 Prompt Details:")
        print(f"   Prompt ID: {saved_prompt.prompt_id}")
        print(f"   Name: {saved_prompt.prompt_name}")
        print(f"   Version: {getattr(saved_prompt, 'version', 'latest')}")
        print(f"   Model: {saved_prompt.model_name}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("   Make sure you have the latest vertexai package:")
        print("   pip install --upgrade vertexai google-cloud-aiplatform")
        return False
        
    except Exception as e:
        print(f"❌ Prompt creation/saving failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Provide helpful troubleshooting
        if "permission" in str(e).lower():
            print("   💡 Permission issue - check IAM roles:")
            print("      - Vertex AI User or Vertex AI Admin")
            print("      - Generative AI Administrator")
        elif "not found" in str(e).lower():
            print("   💡 Resource not found - check:")
            print("      - Project ID is correct")
            print("      - Vertex AI API is enabled")
        elif "quota" in str(e).lower():
            print("   💡 Quota issue - check Vertex AI quotas in console")
        
        import traceback
        traceback.print_exc()
        return False

def load_prompt_from_file(file_path: str) -> tuple:
    """Load prompt data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return (
            data["name"],
            data["content"], 
            data["description"]
        )
        
    except Exception as e:
        print(f"❌ Failed to load prompt file: {e}")
        return None, None, None

def test_prompt_retrieval(prompt_id: str) -> bool:
    """Test retrieving the saved prompt."""
    try:
        from vertexai.preview import prompts
        
        print(f"🔍 Testing prompt retrieval...")
        print(f"   Prompt ID: {prompt_id}")
        
        # Load the saved prompt
        retrieved_prompt = prompts.get(prompt_id=prompt_id)
        
        print("✅ Prompt retrieved successfully!")
        print(f"   Name: {retrieved_prompt.prompt_name}")
        print(f"   Content length: {len(retrieved_prompt.prompt_data)} characters")
        print(f"   Model: {retrieved_prompt.model_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt retrieval failed: {e}")
        return False

def upload_sample_test_prompt():
    """Upload a simple test prompt to verify the API works."""
    
    print("🧪 Uploading Sample Test Prompt")
    print("=" * 35)
    
    # Simple test prompt
    test_prompt_name = "test_prompt_sample"
    test_prompt_content = """You are a helpful AI assistant for testing purposes.

Your job is to respond to user queries in a friendly and professional manner.

When users ask questions:
1. Provide clear, helpful answers
2. Be concise but informative
3. Maintain a positive tone

This is a test prompt created via Python API to verify Vertex AI Prompt Management functionality."""
    
    test_description = "Simple test prompt to verify API functionality"
    
    return create_and_save_prompt(
        prompt_name=test_prompt_name,
        prompt_content=test_prompt_content,
        description=test_description
    )

def upload_from_file(file_choice: str = "1") -> bool:
    """Upload prompt from your generated files."""
    
    prompts_dir = Path("vertex_prompts")
    
    if not prompts_dir.exists():
        print("❌ vertex_prompts directory not found")
        print("   Run 'python create_prompts.py' first")
        return False
    
    # Map choices to files
    prompt_files = {
        "1": "csv_json_converter_prompt.json",
        "2": "test_case_generator_prompt.json",
        "csv": "csv_json_converter_prompt.json",
        "test": "test_case_generator_prompt.json"
    }
    
    if file_choice in prompt_files:
        file_path = prompts_dir / prompt_files[file_choice]
    else:
        file_path = prompts_dir / f"{file_choice}.json"
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    # Load and upload
    prompt_name, prompt_content, description = load_prompt_from_file(file_path)
    
    if not prompt_name:
        return False
    
    return create_and_save_prompt(prompt_name, prompt_content, description)

def list_existing_prompts():
    """List existing prompts in Vertex AI (if possible)."""
    try:
        from vertexai.preview import prompts
        
        print("📋 Attempting to list existing prompts...")
        
        # Try to list prompts (API may not support this yet)
        # This is exploratory code to see what's available
        
        print("⚠️  Prompt listing API not yet available")
        print("   Check prompts in Google Cloud Console:")
        print("   https://console.cloud.google.com/vertex-ai/studio/prompt-management")
        
    except Exception as e:
        print(f"❌ Could not list prompts: {e}")

def main():
    """Main function to upload prompts to Vertex AI."""
    print("🚀 Upload Prompt to Vertex AI Prompt Management")
    print("=" * 55)
    
    # Check credentials
    creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds:
        print("❌ Set credentials first:")
        print('$env:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\to\\key.json"')
        return
    
    print(f"✅ Credentials: {creds}")
    
    # Initialize Vertex AI
    if not setup_vertex_ai():
        return
    
    print("\\nChoose upload option:")
    print("1. Upload simple test prompt (verify API works)")
    print("2. Upload CSV converter prompt from file")
    print("3. Upload test case generator prompt from file") 
    print("4. List existing prompts")
    
    try:
        choice = input("\\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print("\\n" + "="*50)
            success = upload_sample_test_prompt()
            
        elif choice == "2":
            print("\\n" + "="*50)
            success = upload_from_file("1")
            
        elif choice == "3":
            print("\\n" + "="*50)
            success = upload_from_file("2")
            
        elif choice == "4":
            print("\\n" + "="*50)
            list_existing_prompts()
            return
            
        else:
            print("\\nInvalid choice, uploading test prompt...")
            success = upload_sample_test_prompt()
        
        if success:
            print("\\n🎉 SUCCESS!")
            print("\\n📋 Next Steps:")
            print("1. Verify in console: https://console.cloud.google.com/vertex-ai/studio/prompt-management")
            print("2. Test dynamic loading: python test_prompt_loading.py")
            print("3. Deploy agent: python deploy_clean.py")
            
            print("\\n💡 Your agent can now load prompts dynamically!")
            print("   No more hardcoded instructions - update prompts anytime!")
        else:
            print("\\n❌ Upload failed")
            print("\\n🔧 Troubleshooting:")
            print("1. Ensure Vertex AI API is enabled")
            print("2. Check IAM permissions (Vertex AI Admin role)")
            print("3. Verify project ID is correct")
            print("4. Try manual upload in Google Cloud Console")
        
    except (EOFError, KeyboardInterrupt):
        print("\\nUpload cancelled.")

if __name__ == "__main__":
    main()