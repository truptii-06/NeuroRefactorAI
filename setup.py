#!/usr/bin/env python3
"""
NeuroRefactorAI - Automated Setup Script
Handles installation, configuration, and initial setup
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Colors:
    """Terminal colors for pretty output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def check_python_version():
    """Verify Python version"""
    print_header("Checking Python Version")
    version = sys.version_info

    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print_error(f"Python 3.11+ required. Found: {version.major}.{version.minor}")
        print_info("Please upgrade Python: https://www.python.org/downloads/")
        return False

    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_pip():
    """Verify pip is installed"""
    print_header("Checking Package Manager")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                      check=True, capture_output=True)
        print_success("pip is installed")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not installed")
        print_info("Install pip: https://pip.pypa.io/en/stable/installation/")
        return False

def create_virtual_environment():
    """Create virtual environment"""
    print_header("Setting Up Virtual Environment")

    venv_path = Path("venv")

    if venv_path.exists():
        print_warning("Virtual environment already exists")
        response = input("Do you want to recreate it? (y/N): ").lower()
        if response == 'y':
            import shutil
            shutil.rmtree(venv_path)
            print_info("Removed existing virtual environment")
        else:
            print_info("Using existing virtual environment")
            return True

    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def get_pip_command():
    """Get the correct pip command for the current OS"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip")
    else:
        return os.path.join("venv", "bin", "pip")

def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")

    pip_cmd = get_pip_command()

    # Upgrade pip first
    print_info("Upgrading pip...")
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"],
                      check=True, capture_output=True)
        print_success("pip upgraded")
    except subprocess.CalledProcessError:
        print_warning("Could not upgrade pip, continuing...")

    # Install requirements
    print_info("Installing packages (this may take a few minutes)...")
    try:
        result = subprocess.run([pip_cmd, "install", "-r", "requirement.txt"],
                              check=True, capture_output=True, text=True)
        print_success("All dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies")
        print(e.stderr)
        return False

def setup_api_key():
    """Setup Anthropic API key"""
    print_header("API Key Configuration")

    env_file = Path(".env")

    if env_file.exists():
        print_warning(".env file already exists")
        response = input("Do you want to update it? (y/N): ").lower()
        if response != 'y':
            print_info("Skipping API key setup")
            return True

    print_info("You need an Anthropic API key to use this tool")
    print_info("Get your key from: https://console.anthropic.com/")
    print()

    api_key = input("Enter your Anthropic API key (or press Enter to skip): ").strip()

    if not api_key:
        print_warning("API key not configured")
        print_info("You can set it later in the web interface or .env file")
        return True

    try:
        with open(".env", "w") as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}\n")
        print_success("API key saved to .env file")
        return True
    except Exception as e:
        print_error(f"Failed to save API key: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Project Directories")

    directories = [
        "data/input_code",
        "data/output_code",
        "data/dataset",
        "reports",
        "models",
        "notebooks",
        "tests",
        "docs",
        "src/ai"
    ]

    created = 0
    skipped = 0

    for directory in directories:
        try:
            path = Path(directory)
            if path.exists():
                print_info(f"Directory already exists: {directory}")
                skipped += 1
            else:
                path.mkdir(parents=True, exist_ok=True)
                print_success(f"Created: {directory}")
                created += 1
        except Exception as e:
            print_warning(f"Could not create {directory}: {e}")

    if created > 0:
        print_success(f"Created {created} new directories")
    if skipped > 0:
        print_info(f"Skipped {skipped} existing directories")

    return True

def create_init_files():
    """Create __init__.py files"""
    print_header("Setting Up Python Packages")

    init_files = [
        "src/__init__.py",
        "src/ai/__init__.py",
        "src/core/__init__.py",
        "src/inference/__init__.py",
        "src/reports/__init__.py",
        "src/ui/__init__.py",
        "tests/__init__.py"
    ]

    created = 0
    skipped = 0

    for init_file in init_files:
        try:
            path = Path(init_file)
            path.parent.mkdir(parents=True, exist_ok=True)

            if path.exists():
                print_info(f"File already exists: {init_file}")
                skipped += 1
            else:
                path.touch(exist_ok=True)
                print_success(f"Created: {init_file}")
                created += 1
        except Exception as e:
            print_warning(f"Could not create {init_file}: {e}")

    if created > 0:
        print_success(f"Created {created} new __init__.py files")
    if skipped > 0:
        print_info(f"Skipped {skipped} existing files")

    return True

def run_tests():
    """Run basic tests to verify installation"""
    print_header("Running Verification Tests")

    print_info("Testing imports...")

    test_imports = [
        ("streamlit", "Streamlit"),
        ("anthropic", "Anthropic SDK"),
        ("libcst", "LibCST"),
        ("radon", "Radon"),
        ("pytest", "Pytest")
    ]

    all_good = True
    for module, name in test_imports:
        try:
            __import__(module)
            print_success(f"{name} imported successfully")
        except ImportError as e:
            print_error(f"Failed to import {name}: {e}")
            all_good = False

    return all_good

def print_activation_instructions():
    """Print virtual environment activation instructions"""
    print_header("Virtual Environment Activation")

    if platform.system() == "Windows":
        print(f"{Colors.OKCYAN}To activate the virtual environment:{Colors.ENDC}")
        print(f"   {Colors.BOLD}venv\\Scripts\\activate{Colors.ENDC}\n")
        print(f"{Colors.OKCYAN}To deactivate:{Colors.ENDC}")
        print(f"   {Colors.BOLD}deactivate{Colors.ENDC}\n")
    else:
        print(f"{Colors.OKCYAN}To activate the virtual environment:{Colors.ENDC}")
        print(f"   {Colors.BOLD}source venv/bin/activate{Colors.ENDC}\n")
        print(f"{Colors.OKCYAN}To deactivate:{Colors.ENDC}")
        print(f"   {Colors.BOLD}deactivate{Colors.ENDC}\n")

def print_next_steps():
    """Print instructions for next steps"""
    print_header("Setup Complete! 🎉")

    print(f"{Colors.OKGREEN}Installation successful!{Colors.ENDC}")
    print("\nNext steps:\n")

    if platform.system() == "Windows":
        print(f"{Colors.OKCYAN}1. Activate virtual environment:{Colors.ENDC}")
        print(f"   {Colors.BOLD}venv\\Scripts\\activate{Colors.ENDC}\n")
    else:
        print(f"{Colors.OKCYAN}1. Activate virtual environment:{Colors.ENDC}")
        print(f"   {Colors.BOLD}source venv/bin/activate{Colors.ENDC}\n")

    print(f"{Colors.OKCYAN}2. Ensure you have the AI agent code:{Colors.ENDC}")
    print(f"   Create/update: {Colors.BOLD}src/ai/refactoring_agent.py{Colors.ENDC}\n")

    print(f"{Colors.OKCYAN}3. Start the application:{Colors.ENDC}")
    print(f"   {Colors.BOLD}streamlit run app.py{Colors.ENDC}\n")

    print(f"{Colors.OKCYAN}4. Open in browser:{Colors.ENDC}")
    print(f"   {Colors.BOLD}http://localhost:8501{Colors.ENDC}\n")

    if not Path(".env").exists():
        print(f"{Colors.WARNING}⚠ Note:{Colors.ENDC} Remember to configure your Anthropic API key!")
        print(f"      Set it in .env file or through the web interface\n")

    print(f"{Colors.OKCYAN}5. Run tests (optional):{Colors.ENDC}")
    print(f"   {Colors.BOLD}pytest tests/ -v{Colors.ENDC}\n")

    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")

def main():
    """Main setup routine"""
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           🧠 NeuroRefactorAI Setup Script 🧠            ║
║                                                          ║
║          Industry-Level AI Code Refactoring Tool        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)

    steps = [
        ("Python Version", check_python_version),
        ("Package Manager", check_pip),
        ("Virtual Environment", create_virtual_environment),
        ("Dependencies", install_dependencies),
        ("Project Structure", create_directories),
        ("Package Initialization", create_init_files),
        ("API Configuration", setup_api_key),
        ("Verification", run_tests)
    ]

    failed_steps = []

    for step_name, step_func in steps:
        if not step_func():
            failed_steps.append(step_name)
            if step_name in ["Python Version", "Package Manager", "Virtual Environment"]:
                print_error(f"Critical step '{step_name}' failed. Cannot continue.")
                sys.exit(1)

    print_header("Setup Summary")

    if not failed_steps:
        print_success("All steps completed successfully!")
        print_activation_instructions()
        print_next_steps()
    else:
        print_warning("Setup completed with some warnings:")
        for step in failed_steps:
            print(f"  - {step}")
        print("\nThe application should still work, but some features may be limited.")
        print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
