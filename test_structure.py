#!/usr/bin/env python3
"""
Test script to verify the hotel content automation system structure.
This script checks that all necessary files and modules are in place.
"""

import os
import sys
from pathlib import Path

def test_file_structure():
    """Test that all necessary files exist."""
    print("🔍 Testing file structure...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "setup.md",
        "ARCHITECTURE.md",
        "src/__init__.py",
        "src/logger.py",
        "src/google_drive.py",
        "src/google_docs.py",
        "src/openai_handler.py",
        "src/text_designer.py",
        "src/video_editor.py",
        "src/telegram_bot.py",
        "templates/style_guide.json",
    ]
    
    required_dirs = [
        "src",
        "templates",
        "templates/fonts",
        "logs",
    ]
    
    all_ok = True
    
    # Check directories
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  ✅ Directory: {dir_path}")
        else:
            print(f"  ❌ Missing directory: {dir_path}")
            all_ok = False
    
    # Check files
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  ✅ File: {file_path}")
        else:
            print(f"  ❌ Missing file: {file_path}")
            all_ok = False
    
    return all_ok

def test_python_syntax():
    """Test Python files for syntax errors."""
    print("\n🔍 Testing Python syntax...")
    
    python_files = [
        "main.py",
        "src/__init__.py",
        "src/logger.py",
        "src/google_drive.py",
        "src/google_docs.py",
        "src/openai_handler.py",
        "src/text_designer.py",
        "src/video_editor.py",
        "src/telegram_bot.py",
    ]
    
    all_ok = True
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            print(f"  ✅ {file_path}")
        except SyntaxError as e:
            print(f"  ❌ {file_path}: {e}")
            all_ok = False
    
    return all_ok

def test_documentation():
    """Test that documentation files exist and are not empty."""
    print("\n🔍 Testing documentation...")
    
    docs = [
        ("README.md", 1000),
        ("setup.md", 1000),
        ("ARCHITECTURE.md", 1000),
    ]
    
    all_ok = True
    
    for doc_file, min_size in docs:
        if os.path.isfile(doc_file):
            size = os.path.getsize(doc_file)
            if size >= min_size:
                print(f"  ✅ {doc_file} ({size} bytes)")
            else:
                print(f"  ⚠️  {doc_file} ({size} bytes) - might be incomplete")
        else:
            print(f"  ❌ Missing: {doc_file}")
            all_ok = False
    
    return all_ok

def test_env_example():
    """Test .env.example structure."""
    print("\n🔍 Testing .env.example...")
    
    required_vars = [
        "OPENAI_API_KEY",
        "GOOGLE_DRIVE_FOLDER_ID",
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_USER_ID",
        "RAW_VIDEO_FOLDER",
        "RAW_PHOTO_FOLDER",
        "TEXTS_FOLDER",
        "POSTS_REFERENCE_FOLDER",
    ]
    
    all_ok = True
    
    if not os.path.isfile('.env.example'):
        print("  ❌ .env.example not found")
        return False
    
    with open('.env.example', 'r') as f:
        content = f.read()
    
    for var in required_vars:
        if var in content:
            print(f"  ✅ {var}")
        else:
            print(f"  ❌ Missing variable: {var}")
            all_ok = False
    
    return all_ok

def test_requirements():
    """Test requirements.txt."""
    print("\n🔍 Testing requirements.txt...")
    
    required_packages = [
        "python-dotenv",
        "google-auth",
        "google-api-python-client",
        "openai",
        "moviepy",
        "Pillow",
        "python-telegram-bot",
        "requests",
    ]
    
    all_ok = True
    
    if not os.path.isfile('requirements.txt'):
        print("  ❌ requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    for package in required_packages:
        if package in content:
            print(f"  ✅ {package}")
        else:
            print(f"  ❌ Missing package: {package}")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests."""
    print("=" * 80)
    print("Hotel Content Automation - System Verification")
    print("=" * 80)
    
    results = []
    
    results.append(("File Structure", test_file_structure()))
    results.append(("Python Syntax", test_python_syntax()))
    results.append(("Documentation", test_documentation()))
    results.append((".env.example", test_env_example()))
    results.append(("requirements.txt", test_requirements()))
    
    print("\n" + "=" * 80)
    print("Test Results Summary")
    print("=" * 80)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:20s} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 80)
    
    if all_passed:
        print("\n🎉 All tests passed! The system structure is complete.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Fill in your API keys and configuration")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Install FFmpeg (see setup.md)")
        print("5. Run: python main.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
