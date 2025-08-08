#!/usr/bin/env python3
"""
Create and Manage Prompts in Vertex AI Prompt Garden
Helps you set up dynamic prompts for your agents
"""

import os
import json
from pathlib import Path

def create_prompt_templates():
    """Create prompt templates for Vertex AI Prompt Garden."""
    
    print("Creating Prompt Templates for Vertex AI Prompt Garden")
    print("=" * 55)
    
    # Create prompts directory
    prompts_dir = Path("vertex_prompts")
    prompts_dir.mkdir(exist_ok=True)
    
    # CSV to JSON Converter Prompt
    csv_prompt = {
        "name": "csv_json_converter_prompt",
        "display_name": "CSV to JSON Converter Agent Prompt",
        "description": "Professional prompt for CSV to JSON conversion agent with advanced capabilities",
        "content": """You are a professional CSV to JSON converter agent with advanced data processing capabilities.

**Your Core Mission:**
Convert CSV data to clean, well-formatted JSON while providing detailed analysis and insights.

**When users provide CSV data, follow this process:**

1. **Analysis Phase:**
   - Use analyze_csv tool to examine structure, data types, and quality
   - Identify potential issues (missing values, inconsistent formats, etc.)
   - Report column count, row count, and data characteristics

2. **Conversion Phase:**  
   - Use csv_to_json tool to convert data
   - Choose appropriate JSON format (array of objects by default)
   - Handle edge cases and data type preservation

3. **Presentation Phase:**
   - Show clear before/after statistics
   - Display formatted JSON output with proper indentation
   - Highlight any data quality issues or recommendations
   - Provide conversion summary with key metrics

**Quality Standards:**
- Always validate data before conversion
- Preserve data integrity and relationships
- Handle special characters and unicode properly
- Provide helpful error messages for invalid CSV
- Suggest improvements for data quality

**Response Format:**
- Lead with conversion status and key statistics
- Show clean, readable JSON output
- Include actionable insights about the data
- Maintain professional, helpful tone

**Advanced Features:**
- Support different JSON structures (array vs object)
- Handle large datasets efficiently  
- Detect and report data anomalies
- Provide data type recommendations

Be thorough, accurate, and user-focused in all conversions.""",
        "tags": ["csv", "json", "data-conversion", "analytics"],
        "version": "1.0"
    }
    
    # Test Case Generator Prompt
    test_case_prompt = {
        "name": "test_case_generator_prompt",
        "display_name": "Test Case Generator Agent Prompt",
        "description": "Expert prompt for generating comprehensive JIRA-ready test cases",
        "content": """You are an expert Test Case Generation Agent specializing in creating comprehensive, professional test cases from requirements and formatting them for seamless JIRA integration.

**Your Expertise Areas:**
- Functional testing (core features, user workflows)
- UI/UX testing (interface elements, usability)
- API testing (endpoints, data validation, error handling)
- Integration testing (system workflows, data flow)
- Negative testing (edge cases, error scenarios)
- Performance testing (load, stress, scalability)

**When users provide requirements, follow this methodology:**

1. **Requirements Analysis:**
   - Use validate_requirements to assess requirement quality
   - Identify gaps, ambiguities, or missing acceptance criteria
   - Suggest improvements for testability
   - Estimate test coverage and complexity

2. **Test Case Generation:**
   - Use generate_test_cases with appropriate test type
   - Create comprehensive scenarios covering happy path, edge cases, and error conditions
   - Ensure traceability between requirements and test cases
   - Include realistic test data and environment specifications

3. **JIRA Formatting:**
   - Use format_for_jira to create import-ready output
   - Structure test cases with proper JIRA fields
   - Include all necessary metadata (priority, estimates, labels)
   - Provide clear, actionable test steps

**Test Case Quality Standards:**
- **Clear Preconditions:** What must be true before testing
- **Detailed Steps:** Specific, actionable instructions (numbered)
- **Expected Results:** Precise, measurable outcomes
- **Realistic Estimates:** Accurate time and effort projections
- **Proper Prioritization:** Risk-based priority assignment
- **Comprehensive Coverage:** Address all requirement aspects

**JIRA Integration Best Practices:**
- Use standard JIRA field mappings
- Include custom field data where beneficial
- Provide import instructions and field mapping guidance
- Support multiple export formats (CSV preferred, JSON for API import)
- Ensure compatibility with common JIRA configurations

**Response Structure:**
1. Requirements analysis and validation feedback
2. Test case generation summary with coverage metrics
3. Complete JIRA-ready formatted output
4. Step-by-step import instructions
5. Quality assurance recommendations

Focus on creating test cases that will genuinely improve software quality and provide value to QA teams.""",
        "tags": ["testing", "jira", "qa", "test-cases", "requirements"],
        "version": "1.0"
    }
    
    # Save prompts locally
    prompts = [csv_prompt, test_case_prompt]
    
    for prompt in prompts:
        # Save as JSON with metadata
        json_file = prompts_dir / f"{prompt['name']}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(prompt, f, indent=2)
        
        # Save content only as text file
        txt_file = prompts_dir / f"{prompt['name']}.txt"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(prompt["content"])
        
        print(f"✅ Created: {prompt['display_name']}")
        print(f"   Files: {json_file}, {txt_file}")
        print(f"   Length: {len(prompt['content'])} characters")
    
    return prompts_dir

def create_upload_instructions():
    """Create step-by-step instructions for uploading to Prompt Garden."""
    
    instructions = '''# How to Upload Prompts to Vertex AI Prompt Garden

## Step-by-Step Guide

### Option 1: Via Google Cloud Console (Recommended)

1. **Open Google Cloud Console**
   - Go to: https://console.cloud.google.com
   - Select project: vertex-ai-demo-468112

2. **Navigate to Vertex AI**
   - Search for "Vertex AI" 
   - Go to: Vertex AI → Agent Builder → Prompt Gallery
   - Or: https://console.cloud.google.com/vertex-ai/prompt-gallery

3. **Create New Prompt Template**
   - Click "Create Prompt Template"
   - Fill in details:

### For CSV to JSON Converter:
- **Name:** `csv_json_converter_prompt`
- **Display Name:** "CSV to JSON Converter Agent Prompt"  
- **Description:** "Professional prompt for CSV to JSON conversion"
- **Content:** Copy from `vertex_prompts/csv_json_converter_prompt.txt`
- **Tags:** csv, json, data-conversion
- **Save and Publish**

### For Test Case Generator:
- **Name:** `test_case_generator_prompt`
- **Display Name:** "Test Case Generator Agent Prompt"
- **Description:** "Expert prompt for JIRA test case generation"  
- **Content:** Copy from `vertex_prompts/test_case_generator_prompt.txt`
- **Tags:** testing, jira, qa
- **Save and Publish**

## Step 3: Verify Prompts Are Available

Run this test to verify your prompts are accessible:
```bash
python test_prompt_loading.py
```

## Step 4: Deploy Agents with Dynamic Prompts

Your agents will now automatically load prompts from Prompt Garden:
```bash
python deploy_csv_agent.py  # Uses dynamic prompts!
```

## Benefits

✅ **Update prompts without redeploying agents**
✅ **Version control and testing for prompts**  
✅ **Team collaboration on prompt optimization**
✅ **Centralized prompt management**
✅ **A/B testing different prompt variations**

## Troubleshooting

**If dynamic loading fails:**
- Check prompt names match exactly
- Verify Vertex AI API permissions
- Ensure Prompt Garden is available in your region
- Agents will fall back to static prompts automatically

**Common issues:**
- Prompt Garden may be in preview/beta
- API endpoints may vary by region
- Permission requirements may change

Your agents are designed to work with or without Prompt Garden!
'''
    
    with open("PROMPT_GARDEN_INSTRUCTIONS.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("✅ Created PROMPT_GARDEN_INSTRUCTIONS.md")

def create_prompt_management_script():
    """Create script to manage prompts programmatically."""
    
    management_script = '''#!/usr/bin/env python3
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
        print(f"\\n" + "-" * 40)
        upload_prompt_to_garden(prompt_file)
    
    print(f"\\n🎉 Prompt management complete!")
    print(f"\\nNext steps:")
    print(f"1. Verify prompts in Vertex AI Console")
    print(f"2. Test dynamic loading: python test_prompt_loading.py") 
    print(f"3. Deploy agents: python deploy_csv_agent.py")

if __name__ == "__main__":
    main()
'''
    
    with open("manage_prompts.py", "w", encoding="utf-8") as f:
        f.write(management_script)
    
    print("✅ Created manage_prompts.py")

def main():
    """Main setup function."""
    print("🔄 Vertex AI Prompt Garden Setup")
    print("=" * 40)
    print("Setting up dynamic prompt loading for your agents")
    print()
    
    # Create prompt templates
    prompts_dir = create_prompt_templates()
    
    # Create instructions
    create_upload_instructions()
    
    # Create management script
    create_prompt_management_script()
    
    print(f"\n🎉 Prompt Garden Setup Complete!")
    print(f"\n📁 Files Created:")
    print(f"   📂 {prompts_dir}/ - Prompt template files")
    print(f"   📄 PROMPT_GARDEN_INSTRUCTIONS.md - Setup guide")
    print(f"   📄 manage_prompts.py - Prompt management script")
    
    print(f"\n📋 Next Steps:")
    print(f"1. **Read the setup guide:**")
    print(f"   📖 Open PROMPT_GARDEN_INSTRUCTIONS.md")
    
    print(f"\n2. **Upload prompts to Vertex AI:**")
    print(f"   🌐 Go to Google Cloud Console → Vertex AI → Prompt Gallery")
    print(f"   📋 Copy content from vertex_prompts/*.txt files")
    
    print(f"\n3. **Test dynamic loading:**")
    print(f"   🧪 python test_prompt_loading.py")
    
    print(f"\n4. **Deploy agents with dynamic prompts:**")
    print(f"   🚀 python deploy_csv_agent.py")
    
    print(f"\n✨ Benefits of Dynamic Prompts:")
    print(f"   ✅ Update agent behavior without redeployment")
    print(f"   ✅ A/B testing and prompt optimization")
    print(f"   ✅ Team collaboration on agent improvement")
    print(f"   ✅ Version control for prompt changes")
    
    print(f"\n🎯 Your Dynamic Prompt System is Ready!")

if __name__ == "__main__":
    main()