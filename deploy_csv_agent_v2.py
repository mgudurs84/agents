#!/usr/bin/env python3
"""
Clean CSV to JSON Agent Deployment Script
Uses gcloud login instead of service account key files
"""

import os
import sys
import subprocess
import json

PROJECT_ID = "vertex-ai-demo-468112"  # CHANGE THIS
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
            print(f"Required project: {PROJECT_ID}")
            
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
            print(f"Project correctly set: {PROJECT_ID}")
    
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

def list_available_buckets():
    """List available buckets in the organization."""
    print("\nListing Available Buckets")
    print("=" * 32)
    
    try:
        from google.cloud import storage
        storage_client = storage.Client(project=PROJECT_ID)
        
        buckets = list(storage_client.list_buckets())
        
        if not buckets:
            print("No buckets found in this project")
            return []
        
        print("Available buckets:")
        bucket_names = []
        for i, bucket in enumerate(buckets, 1):
            print(f"  {i}. {bucket.name}")
            bucket_names.append(bucket.name)
        
        return bucket_names
        
    except Exception as e:
        print(f"Failed to list buckets: {e}")
        return []

def select_staging_bucket():
    """Let user select or create a staging bucket."""
    print("\nStaging Bucket Selection")
    print("=" * 30)
    
    # List existing buckets
    bucket_names = list_available_buckets()
    
    if bucket_names:
        print("\nOptions:")
        print("1. Use existing bucket")
        print("2. Create new bucket")
        
        try:
            choice = input("\nChoose option (1/2): ").strip()
            
            if choice == "1":
                print("\nSelect a bucket:")
                for i, name in enumerate(bucket_names, 1):
                    print(f"  {i}. {name}")
                
                try:
                    bucket_choice = int(input(f"\nEnter bucket number (1-{len(bucket_names)}): "))
                    if 1 <= bucket_choice <= len(bucket_names):
                        selected_bucket = bucket_names[bucket_choice - 1]
                        print(f"Selected bucket: {selected_bucket}")
                        return f"gs://{selected_bucket}"
                    else:
                        print("Invalid selection")
                        return None
                except (ValueError, EOFError, KeyboardInterrupt):
                    print("Invalid selection")
                    return None
            
            elif choice == "2":
                # Create new bucket
                bucket_name = f"{PROJECT_ID}-vertex-ai-staging"
                print(f"Will create new bucket: {bucket_name}")
                return f"gs://{bucket_name}"
            
            else:
                print("Invalid choice")
                return None
                
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled bucket selection")
            return None
    else:
        # No existing buckets, create new one
        bucket_name = f"{PROJECT_ID}-vertex-ai-staging"
        print(f"No existing buckets found")
        print(f"Will create new bucket: {bucket_name}")
        return f"gs://{bucket_name}"

def setup_environment():
    """Setup environment using gcloud authentication."""
    print("\nEnvironment Setup")
    print("=" * 25)
    
    # Remove any existing service account credentials environment variable
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        print("Removing GOOGLE_APPLICATION_CREDENTIALS environment variable")
        del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    
    # Set project ID in environment
    os.environ['GOOGLE_CLOUD_PROJECT'] = PROJECT_ID
    print(f"Project ID: {PROJECT_ID}")
    
    # Verify we can access Google Cloud with current credentials
    try:
        from google.auth import default
        credentials, project = default()
        
        if project != PROJECT_ID:
            print(f"Warning: Default project ({project}) differs from target ({PROJECT_ID})")
            print("This is usually fine as we've set the project explicitly")
        
        print("Application Default Credentials found and working")
        return True
        
    except Exception as e:
        print(f"Failed to get default credentials: {e}")
        print("\nPlease ensure you've run:")
        print("1. gcloud auth login")
        print("2. gcloud auth application-default login")
        print(f"3. gcloud config set project {PROJECT_ID}")
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

def ensure_bucket_exists(bucket_uri):
    """Ensure the specified bucket exists and is accessible."""
    bucket_name = bucket_uri.replace("gs://", "")
    
    try:
        from google.cloud import storage
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        
        if bucket.exists():
            print(f"Bucket {bucket_name} exists and is accessible")
            return True
        else:
            print(f"Creating bucket {bucket_name}...")
            try:
                bucket = storage_client.create_bucket(bucket_name, location=LOCATION)
                print(f"Bucket {bucket_name} created successfully")
                return True
            except Exception as create_error:
                print(f"Failed to create bucket: {create_error}")
                return False
            
    except Exception as e:
        print(f"Bucket access error: {e}")
        return False

def deploy_with_agent_engines(agent, staging_bucket):
    """Deploy using agent engines (preferred method)."""
    print("\nDeploying with Agent Engines")
    print("=" * 35)
    
    try:
        import vertexai
        from vertexai.preview import reasoning_engines
        from vertexai import agent_engines
        
        # Initialize Vertex AI with selected bucket
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=staging_bucket
        )
        print(f"Vertex AI initialized with staging bucket: {staging_bucket}")
        
        # Ensure bucket exists and is accessible
        if not ensure_bucket_exists(staging_bucket):
            print("Bucket setup failed")
            return None
        
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

def deploy_with_reasoning_engines(agent, staging_bucket):
    """Deploy using reasoning engines (fallback method)."""
    print("\nDeploying with Reasoning Engines")
    print("=" * 40)
    
    try:
        import vertexai
        from vertexai.preview import reasoning_engines
        
        # Initialize Vertex AI with selected bucket
        vertexai.init(
            project=PROJECT_ID,
            location=LOCATION,
            staging_bucket=staging_bucket
        )
        print(f"Vertex AI initialized with staging bucket: {staging_bucket}")
        
        # Ensure bucket exists and is accessible
        if not ensure_bucket_exists(staging_bucket):
            print("Bucket setup failed")
            return None
        
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
    print("CSV to JSON Agent - Clean Deployment (gcloud login)")
    print("=" * 55)
    print(f"Project: {PROJECT_ID}")
    print(f"Location: {LOCATION}")
    print()
    
    # Step 1: Check gcloud authentication
    print("Step 1: Checking gcloud authentication...")
    if not check_gcloud_auth():
        print("\nAuthentication setup failed")
        print("\nQuick setup commands:")
        print("1. gcloud auth login")
        print("2. gcloud auth application-default login") 
        print(f"3. gcloud config set project {PROJECT_ID}")
        return
    
    # Step 2: Fix dependencies
    print("\nStep 2: Fixing dependency conflicts...")
    if not fix_dependencies():
        print("Dependency fixing failed")
        return
    
    # Step 3: Verify imports
    print("Step 3: Verifying imports...")
    has_agent_engines = verify_imports()
    if not has_agent_engines:
        print("agent_engines not available, will use reasoning engines")
    
    # Step 4: Select staging bucket
    print("Step 4: Selecting staging bucket...")
    staging_bucket = select_staging_bucket()
    if not staging_bucket:
        print("Bucket selection failed")
        return
    
    # Step 5: Setup environment
    print("Step 5: Setting up environment...")
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
        print(f"\nDeployment Summary:")
        print(f"  Project: {PROJECT_ID}")
        print(f"  Location: {LOCATION}")
        print(f"  Staging Bucket: {staging_bucket}")
        
        confirm = input(f"\nDeploy CSV to JSON Agent to Vertex AI? (yes/no): ").strip().lower()
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
        deployed_agent = deploy_with_agent_engines(agent, staging_bucket)
    
    if not deployed_agent:
        print("Falling back to Reasoning Engines...")
        deployed_agent = deploy_with_reasoning_engines(agent, staging_bucket)
    
    if deployed_agent:
        print("\nSUCCESS!")
        print("\nUsage Examples:")
        print("   Send CSV data like:")
        print("   name,age,city")
        print("   John,25,NYC")
        print("   Jane,30,LA")
        
        print(f"\nResource: {deployed_agent.resource_name}")
        print("Console: https://console.cloud.google.com/vertex-ai/agents")
    else:
        print("\nAll deployment methods failed - check errors above")

if __name__ == "__main__":
    main()