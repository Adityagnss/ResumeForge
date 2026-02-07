#!/usr/bin/env python3
"""
Quick diagnostic script to verify ResumeForge setup.
Run this to check if everything is configured correctly.
"""

import os
import sys
from pathlib import Path

def test_setup():
    """Run diagnostic tests on the ResumeForge setup."""
    
    print("🔍 ResumeForge Configuration Diagnostics\n")
    print("=" * 50)
    
    # Test 1: Check .env file
    print("\n1. Checking .env file...")
    env_file = Path(".env")
    if env_file.exists():
        print("   ✅ .env file exists")
        with open(env_file) as f:
            content = f.read()
            if "GOOGLE_API_KEY" in content:
                print("   ✅ GOOGLE_API_KEY is set")
            else:
                print("   ❌ GOOGLE_API_KEY not found in .env")
                return False
    else:
        print("   ❌ .env file not found")
        return False
    
    # Test 2: Load environment variables
    print("\n2. Loading environment variables...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            print(f"   ✅ API Key loaded: {api_key[:20]}...")
        else:
            print("   ❌ API Key not loaded")
            return False
    except ImportError:
        print("   ⚠️  python-dotenv not installed (optional)")
    
    # Test 3: Check required packages
    print("\n3. Checking required packages...")
    try:
        import google.adk
        print(f"   ✅ google-adk installed (version: {google.adk.__version__})")
    except ImportError:
        print("   ❌ google-adk not installed")
        return False
    
    try:
        import pydantic
        print(f"   ✅ pydantic installed (version: {pydantic.__version__})")
    except ImportError:
        print("   ❌ pydantic not installed")
        return False
    
    # Test 4: Check resume.json
    print("\n4. Checking resume.json...")
    resume_file = Path("resume.json")
    if resume_file.exists():
        print("   ✅ resume.json exists")
        try:
            import json
            from schema import Resume
            with open(resume_file) as f:
                data = json.load(f)
            Resume(**data)
            print("   ✅ resume.json is valid")
        except Exception as e:
            print(f"   ❌ resume.json validation failed: {e}")
            return False
    else:
        print("   ❌ resume.json not found")
        return False
    
    # Test 5: Load agents
    print("\n5. Loading agents...")
    try:
        from agents.unibot import unibot
        print(f"   ✅ Root agent loaded: {unibot.name}")
        print(f"   ✅ Model: {unibot.model}")
        print(f"   ✅ Sub-agents: {[a.name for a in unibot.sub_agents]}")
    except Exception as e:
        print(f"   ❌ Failed to load agents: {e}")
        return False
    
    # Test 6: Check tools
    print("\n6. Checking tools...")
    try:
        from tools import get_resume, get_summary, add_skill
        print("   ✅ Tools imported successfully")
        
        # Test a read operation
        summary = get_summary()
        print(f"   ✅ Tools working (summary length: {len(summary)} chars)")
    except Exception as e:
        print(f"   ❌ Tools check failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All checks passed! ResumeForge is ready to use.\n")
    print("To run the agent:")
    print("  • Web UI:  adk web")
    print("  • CLI:     adk run")
    print()
    return True

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)
