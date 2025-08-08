# How to Upload Prompts to Vertex AI Prompt Garden

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
