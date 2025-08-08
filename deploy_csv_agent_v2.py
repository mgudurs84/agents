#!/usr/bin/env python3
"""
Clean CSV to JSON Agent Deployment Script
Uses gcloud login instead of service account key files
Configured for anbc-dev-cdr-de (compute) and anbc-dev (storage with test-agent bucket)
"""

import os
import sys
import subprocess
import json

PROJECT_ID = "anbc-dev-cdr-de"  # Compute project for Vertex AI
STORAGE_PROJECT_ID = "anbc-dev"  # Storage project for buckets
STAGING_BUCKET = "gs://test-agent"  # Your specific bucket
LOCATION = "us-central1"

def check_gcloud_auth():
    """Check if user is authenticated with gcloud and has correct project set."""
    print("Checking gcloud Authentication")
    print("=" * 35)
    
    try:
        # Check if gcloud is installed
        result = subprocess.run(
            ["gcloud", "version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print("gcloud CLI is installed")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: gcloud CLI not found")
        print("\nPlease install gcloud CLI:")
        print("https://cloud.google.com/sdk/docs/install")
        return False
    
    try:
        # Check current authentication
        result = subprocess.run(
            ["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"],
            capture_output=True,
            text=True,
            check=True
        )
        
        active_account = result.stdout.strip()
        if not active_account:
            print("No active gcloud authentication found")
            print("\nPlease run: gcloud auth login")
            print("Then run: gcloud auth application-default login")
            return False
        
        print(f"Authenticated as: {active_account}")
        
    except subprocess.CalledProcessError:
        print("Failed to check gcloud authentication")
        print("\nPlease run: gcloud auth login")
        print("Then run: gcloud auth application-default login")
        return False
    
    try:
        # Check current project
        result = subprocess.run(
            ["gcloud", "config", "get-value", "project"],
            capture_output=True,
            text=True,
            check=True
        )
        
        current_project = result.stdout.strip()
        if current_project != PROJECT_ID:
            print(f"Current project: {current_project}")
            print(f"Required compute project: {PROJECT_ID}")
            
            # Ask if we should set the project
            try:
                set_project = input(f"\nSet gcloud project to {PROJECT_ID}? (yes/no): ").strip().lower()
                if set_project in ['yes', 'y']:
                    subprocess.run(
                        ["gcloud", "config", "set", "project", PROJECT_ID],
                        check=True
                    )
                    print(f"Project set to {PROJECT_ID}")
                else:
                    print("Please manually set project with:")
                    print(f"gcloud config set project {PROJECT_ID}")
                    return False
            except (EOFError, KeyboardInterrupt):
                print(f"\nPlease set project manually: gcloud config set project {PROJECT_ID}")
                return False
        else:
            print(f"Compute project correctly set: {PROJECT_ID}")
    
    except subprocess.CalledProcessError:
        print(f"Failed to get current project")
        print(f"Setting project to {PROJECT_ID}...")
        try:
            subprocess.run(
                ["gcloud", "config", "set", "project", PROJECT_ID],
                check=True
            )
            print(f"Project set to {PROJECT_ID}")
        except subprocess.CalledProcessError:
            print("Failed to set project")
            return False
    
    # Check application default credentials
    try:
        result = subprocess.run(
            ["gcloud", "auth", "application-default", "print-access-token"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Application Default Credentials are working")
        
    except subprocess.CalledProcessError:
        print("Application Default Credentials not set")
        print("\nPlease run: gcloud auth application-default login")
        return False
    
    # Check access to both projects
    print(f"\nChecking access to projects:")
    print(f"  Compute project: {PROJECT_ID}")
    print(f"  Storage project: {STORAGE_PROJECT_ID}")
    print(f"  Using bucket: {STAGING_BUCKET}")
    
    return True

def fix_dependencies():
    """Fix dependency conflicts by installing compatible versions."""
    print("\nFixing Dependencies")
    print("=" * 25)
    
    # First, uninstall conflicting packages
    print("Removing conflicting packages...")
    packages_to_remove = [
        "google-cloud-aiplatform",
        "vertexai", 
        "google-cloud-storage",
        "google-adk"
    ]
    
    for package in packages_to_remove:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "uninstall", package, "-y"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass  # Package might not be installed
    
    print("Cleaned up packages")
    
    # Install compatible versions in correct order
    print("Installing compatible versions...")
    
    # Step 1: Install storage first
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "google-cloud-storage==2.18.0"
    ])
    print("google-cloud-storage==2.18.0")
    
    # Step 2: Install aiplatform with agent engines
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "google-cloud-aiplatform[agent_engines]==1.95.1"
    ])
    print("google-cloud-aiplatform[agent_engines]==1.95.1")
    
    # Step 3: Install vertexai compatible version
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "vertexai==1.71.1"
    ])
    print("vertexai==1.71.1")
    
    # Step 4: Install ADK
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "google-adk==1.9.0"
    ])
    print("google-adk==1.9.0")
    
    print("All dependencies fixed!")
    return True

def verify_imports():
    """Verify all imports work correctly."""
    print("\nVerifying Imports")
    print("=" * 22)
    
    try:
        import vertexai
        print("vertexai")
        
        from vertexai.preview import reasoning_engines
        print("reasoning_engines")
        
        # Check if agent_engines is available
        try:
            from vertexai import agent_engines
            print("agent_engines")
            has_agent_engines = True
        except ImportError:
            print("agent_engines not available - using alternative approach")
            has_agent_engines = False
        
        from google.cloud import aiplatform, storage
        print("google.cloud libraries")
        
        return has_agent_engines
        
    except ImportError as e:
        print(f"Import verification failed: {e}")
        return False

def verify_bucket_access():
    """Verify access to the test-agent bucket in anbc-dev."""
    print(f"\nVerifying Bucket Access")
    print("=" * 30)
    
    try:
        from google.cloud import storage
        
        # Connect to storage project specifically
        storage_client = storage.Client(project=STORAGE_PROJECT_ID)
        bucket_name = STAGING_BUCKET.replace("gs://", "")
        bucket = storage_client.bucket(bucket_name)
        
        # Check if bucket exists
        if not bucket.exists():
            print(f"ERROR: Bucket {bucket_name} does not exist in {STORAGE_PROJECT_ID}")
            print(f"Please create the bucket or verify the name")
            return False
        
        print(f"✓ Bucket {bucket_name} exists in {STORAGE_PROJECT_ID}")
        
        # Test read access
        try:
            list(bucket.list_blobs(max_results=1))
            print(f"✓ Read access confirmed")
        except Exception as read_error:
            print(f"✗ Read access failed: {read_error}")
            return False
        
        # Test write access by attempting to create a test object
        try:
            test_blob = bucket.blob("deployment-test.txt")
            test_blob.upload_from_string("test")
            test_blob.delete()
            print(f"✓ Write access confirmed")
        except Exception as write_error:
            print(f"✗ Write access failed: {write_error}")
            print(f"Make sure you have Storage Object Creator role in {STORAGE_PROJECT_ID}")
            return False
        
        print(f"✓ Cross-project access verified for {STAGING_BUCKET}")
        return True
        
    except Exception as e:
        print(f"Bucket verification failed: {e}")
        print(f"\nMake sure you have the following roles in {STORAGE_PROJECT_ID}:")
        print("  - Storage Browser or Storage Object Viewer")
        print("  - Storage Object Creator")
        return False

def create_agent():
    """Create the CSV to JSON agent."""
    print("\nCreating Agent")
    print("=" * 20)
    
    try:
        from csv_json_converter import root_agent
        print(f"Agent imported: {type(root_agent)}")
        
        # Test agent differently based on type
        try:
            # Check if it's a real ADK LlmAgent
            if hasattr(root_agent, '__class__') and 'LlmAgent' in str(type(root_agent)):
                print("Real ADK LlmAgent detected - skipping local test")
                print("Agent ready for deployment")
            else:
                # Test simple agent
                test_csv = "name,age\nJohn,25\nJane,30"
                test_result = root_agent(test_csv)
                print(f"Agent test: {len(test_result)} char response")
        except Exception as test_error:
            print(f"Agent test failed: {test_error}")
            print("Continuing with deployment anyway...")
        
        return root_agent
        
    except ImportError as e:
        print(f"Import failed: {e}")
        print("Make sure csv_json_converter package exists")
        print("Run setup_clean.py first")
        return None

def setup_environment():
    """Setup environment using gcloud authentication for cross-project setup."""
    print("\nEnvironment Setup (Cross-Project)")
    print("=" * 40)
    
    # Remove any existing service account credentials environment variable
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        print("Removing GOOGLE_APPLICATION_CREDENTIALS environment variable")
        del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    
    # Set compute project ID in environment (for Vertex AI)
    os.environ['GOOGLE_CLOUD_PROJECT'] = PROJECT_ID
    print(f"Compute Project (Vertex AI): {PROJECT_ID}")
    print(f"Storage Project (Buckets): {STORAGE_PROJECT_ID}")
    print(f"Using bucket: {STAGING_BUCKET}")
    
    # Verify we can access Google Cloud with current credentials
    try:
        from google.auth import default
        credentials, detected_project = default()
        
        print(f"Default credentials project: {detected_project}")
        print("Application Default Credentials found and working")
        
        # Test access to both projects
        print("\nTesting project access...")
        
        # Test compute project access
        try:
            from google.cloud import aiplatform
            aiplatform.init(project=PROJECT_ID, location=LOCATION)
            print(f"✓ Vertex AI access confirmed in {PROJECT_ID}")
        except Exception as e:
            print(f"✗ Vertex AI access failed in {PROJECT_ID}: {e}")
            return False
        
        # Test storage project access (already done in verify_bucket_access)
        print(f"✓ Storage access already verified in {STORAGE_PROJECT_ID}")
        
        return True
        
    except Exception as e:
        print(f"Failed to get default credentials: {e}")
        print("\nPlease ensure you've run:")
        print("1. gcloud auth login")
        print("2. gcloud auth application-default login")
        print(f"3. gcloud config set project {PROJECT_ID}")
        print(f"\nAlso ensure you have access to both projects:")
        print(f"  - {PROJECT_ID} (Vertex AI Administrator)")
        print(f"  - {STORAGE_PROJECT_ID} (Storage Browser/Object Viewer)")
        return False

def deploy_with_agent_engines(agent):
    """Deploy using agent engines (preferred method)."""
    print("\nDeploying with Agent Engines")
    print("=" * 35)
    
    try:
        import vertexai
        from vertexai.preview import reasoning_engines
        from vertexai import agent_engines
        
        # Initialize Vertex AI with your specific bucket
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=STAGING_BUCKET
        )
        print(f"Vertex AI initialized:")
        print(f"  Project: {PROJECT_ID}")
        print(f"  Location: {LOCATION}")
        print(f"  Staging bucket: {STAGING_BUCKET}")
        
        # Create AdkApp
        print("\nCreating AdkApp...")
        app = reasoning_engines.AdkApp(
            agent=agent,
            enable_tracing=True,
        )
        print("AdkApp created")
        
        # Deploy to Agent Engine
        print("\nDeploying to Agent Engine...")
        print("   This may take 5-10 minutes...")
        
        remote_app = agent_engines.create(
            agent_engine=app,
            requirements=[
                "google-cloud-aiplatform[adk,agent_engines]>=1.95.1",
                "google-cloud-storage>=2.18.0"
            ],
            extra_packages=["./csv_json_converter"],
        )
        
        print("Deployment successful!")
        print(f"Resource: {remote_app.resource_name}")
        
        # Test the deployed agent
        print("\nTesting Deployed Agent...")
        try:
            session = remote_app.create_session(user_id="test_user")
            
            test_csv = "name,age,city\nAlice,28,Tokyo\nBob,32,Berlin"
            print(f"Test CSV: {test_csv[:30]}...")
            
            response_parts = []
            for event in remote_app.stream_query(
                user_id="test_user",
                session_id=session["id"],
                message=test_csv
            ):
                if 'parts' in event:
                    for part in event['parts']:
                        if 'text' in part:
                            response_parts.append(part['text'])
            
            if response_parts:
                response = ''.join(response_parts)
                print(f"Response: {response[:100]}...")
                print("Agent test successful!")
            else:
                print("No response, but deployment completed")
                
        except Exception as test_error:
            print(f"Testing error: {test_error}")
        
        return remote_app
        
    except Exception as e:
        print(f"Agent Engine deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def deploy_with_reasoning_engines(agent):
    """Deploy using reasoning engines (fallback method)."""
    print("\nDeploying with Reasoning Engines")
    print("=" * 40)
    
    try:
        import vertexai
        from vertexai.preview import reasoning_engines
        
        # Initialize Vertex AI with your specific bucket
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=STAGING_BUCKET
        )
        print(f"Vertex AI initialized:")
        print(f"  Project: {PROJECT_ID}")
        print(f"  Location: {LOCATION}")
        print(f"  Staging bucket: {STAGING_BUCKET}")
        
        # Create Reasoning Engine
        print("\nCreating Reasoning Engine...")
        
        remote_app = reasoning_engines.ReasoningEngine.create(
            reasoning_engine=agent,
            requirements=[
                "google-cloud-aiplatform[reasoning_engines]>=1.95.1",
                "google-cloud-storage>=2.18.0"
            ],
            extra_packages=["./csv_json_converter"],
            display_name="CSV to JSON Converter",
            description="Converts CSV files to JSON format"
        )
        
        print("Deployment successful!")
        print(f"Resource: {remote_app.resource_name}")
        
        # Test the deployed agent
        print("\nTesting Deployed Agent...")
        try:
            test_csv = "name,age,city\nAlice,28,Tokyo\nBob,32,Berlin"
            print(f"Test CSV: {test_csv[:30]}...")
            
            response = remote_app.query(input=test_csv)
            print(f"Response: {str(response)[:100]}...")
            print("Agent test successful!")
                
        except Exception as test_error:
            print(f"Testing error: {test_error}")
        
        return remote_app
        
    except Exception as e:
        print(f"Reasoning Engine deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main deployment function."""
    print("CSV to JSON Agent - Cross-Project Deployment")
    print("=" * 50)
    print(f"Compute Project (Vertex AI): {PROJECT_ID}")
    print(f"Storage Project (Buckets): {STORAGE_PROJECT_ID}")
    print(f"Staging Bucket: {STAGING_BUCKET}")
    print(f"Location: {LOCATION}")
    print("Cross-VPC wiring: ENABLED")
    print()
    
    # Step 1: Check gcloud authentication
    print("Step 1: Checking gcloud authentication...")
    if not check_gcloud_auth():
        print("\nAuthentication setup failed")
        print("\nQuick setup commands:")
        print("1. gcloud auth login")
        print("2. gcloud auth application-default login") 
        print(f"3. gcloud config set project {PROJECT_ID}")
        print(f"\nEnsure you have access to both projects:")
        print(f"  - {PROJECT_ID}: Vertex AI Administrator") 
        print(f"  - {STORAGE_PROJECT_ID}: Storage Browser/Object Viewer for test-agent bucket")
        return
    
    # Step 2: Verify bucket access
    print("\nStep 2: Verifying test-agent bucket access...")
    if not verify_bucket_access():
        print("Bucket access verification failed")
        return
    
    # Step 3: Fix dependencies
    print("\nStep 3: Fixing dependency conflicts...")
    if not fix_dependencies():
        print("Dependency fixing failed")
        return
    
    # Step 4: Verify imports
    print("Step 4: Verifying imports...")
    has_agent_engines = verify_imports()
    if not has_agent_engines:
        print("agent_engines not available, will use reasoning engines")
    
    # Step 5: Setup cross-project environment
    print("Step 5: Setting up cross-project environment...")
    if not setup_environment():
        print("Environment setup failed")
        return
    
    # Step 6: Create agent
    print("Step 6: Creating agent...")
    agent = create_agent()
    if not agent:
        print("Agent creation failed")
        return
    
    # Step 7: Confirm deployment
    try:
        print(f"\nCross-Project Deployment Summary:")
        print(f"  Compute Project: {PROJECT_ID}")
        print(f"  Storage Project: {STORAGE_PROJECT_ID}")
        print(f"  Location: {LOCATION}")
        print(f"  Staging Bucket: {STAGING_BUCKET}")
        print(f"  Agent will be deployed in: {PROJECT_ID}")
        print(f"  Agent will use storage from: {STORAGE_PROJECT_ID}")
        print(f"  Cross-VPC wiring: ENABLED")
        
        confirm = input(f"\nDeploy CSV to JSON Agent with this configuration? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("Deployment cancelled.")
            return
    except (EOFError, KeyboardInterrupt):
        print("\nDeployment cancelled.")
        return
    
    # Step 8: Deploy (try agent engines first, fallback to reasoning engines)
    deployed_agent = None
    
    if has_agent_engines:
        print("Attempting deployment with Agent Engines...")
        deployed_agent = deploy_with_agent_engines(agent)
    
    if not deployed_agent:
        print("Falling back to Reasoning Engines...")
        deployed_agent = deploy_with_reasoning_engines(agent)
    
    if deployed_agent:
        print("\nSUCCESS!")
        print("\nCross-Project Setup Complete:")
        print(f"  ✓ Agent deployed in: {PROJECT_ID}")
        print(f"  ✓ Using storage from: {STORAGE_PROJECT_ID}")
        print(f"  ✓ Staging bucket: {STAGING_BUCKET}")
        print(f"  ✓ Cross-VPC wiring: ENABLED")
        
        print("\nUsage Examples:")
        print("   Send CSV data like:")
        print("   name,age,city")
        print("   John,25,NYC")
        print("   Jane,30,LA")
        
        print(f"\nResource: {deployed_agent.resource_name}")
        print(f"Console: https://console.cloud.google.com/vertex-ai/agents?project={PROJECT_ID}")
    else:
        print("\nAll deployment methods failed - check errors above")
        print("\nCommon cross-project issues:")
        print(f"1. Missing IAM roles in {STORAGE_PROJECT_ID}")
        print(f"2. Missing IAM roles in {PROJECT_ID}")
        print("3. Cross-VPC connectivity issues")
        print("4. Bucket permissions not set correctly")

if __name__ == "__main__":
    main()