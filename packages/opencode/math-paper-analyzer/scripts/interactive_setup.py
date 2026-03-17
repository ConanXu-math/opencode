#!/usr/bin/env python3
"""Interactive setup wizard for math paper analyzer."""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_step(step: int, total: int, text: str):
    """Print step information."""
    print(f"\n[{step}/{total}] {text}")


def ask_yes_no(question: str, default: bool = True) -> bool:
    """Ask a yes/no question."""
    options = "[Y/n]" if default else "[y/N]"
    while True:
        response = input(f"{question} {options}: ").strip().lower()
        if not response:
            return default
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please enter 'y' or 'n'")


def ask_input(question: str, default: str = "") -> str:
    """Ask for input with optional default."""
    if default:
        prompt = f"{question} [{default}]: "
    else:
        prompt = f"{question}: "

    response = input(prompt).strip()
    return response if response else default


def check_python_dependency(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def install_python_dependency(package: str) -> bool:
    """Install a Python package."""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False


def detect_llm_config() -> Dict[str, Optional[str]]:
    """Detect existing LLM configuration."""
    config = {
        "api_key": None,
        "base_url": None,
        "model": None,
    }

    # Check environment variables
    env_vars = {
        "api_key": ["OPENAI_API_KEY", "LLM_API_KEY"],
        "base_url": ["OPENAI_BASE_URL", "LLM_BASE_URL"],
        "model": ["OPENAI_MODEL", "LLM_MODEL_ID"],
    }

    for key, var_names in env_vars.items():
        for var_name in var_names:
            value = os.getenv(var_name)
            if value:
                config[key] = value
                break

    return config


def save_config(config: Dict, config_path: Path):
    """Save configuration to file."""
    config_path.parent.mkdir(exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✓ Configuration saved to {config_path}")


def load_config(config_path: Path) -> Dict:
    """Load configuration from file."""
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def setup_dependencies():
    """Setup Python dependencies."""
    print_step(1, 4, "Checking dependencies")

    dependencies = [
        ("pymupdf", "fitz", "PyMuPDF for PDF processing"),
        ("openai", "openai", "OpenAI client for LLM"),
        ("httpx", "httpx", "HTTP client for OCR API"),
    ]

    missing_deps = []
    for package, import_name, description in dependencies:
        if check_python_dependency(import_name):
            print(f"✓ {package} ({description}) is installed")
        else:
            print(f"✗ {package} ({description}) is missing")
            missing_deps.append(package)

    if missing_deps:
        print(f"\nMissing dependencies: {', '.join(missing_deps)}")
        if ask_yes_no("Do you want to install missing dependencies?", True):
            for package in missing_deps:
                if not install_python_dependency(package):
                    print(f"Failed to install {package}. Please install manually.")
                    return False
        else:
            print("Please install dependencies manually:")
            print("  pip install pymupdf openai httpx")
            return False

    return True


def setup_ocr_config():
    """Setup OCR configuration."""
    print_step(2, 4, "Configuring OCR service")

    default_ocr_url = "https://edusys5.sii.edu.cn/ocr"
    print(f"Default OCR URL: {default_ocr_url}")

    if ask_yes_no("Use default OCR service?", True):
        ocr_url = default_ocr_url
    else:
        ocr_url = ask_input("Enter OCR API URL", default_ocr_url)

    return {"ocr_url": ocr_url}


def setup_llm_config():
    """Setup LLM configuration interactively."""
    print_step(3, 4, "Configuring LLM service")

    # Detect existing configuration
    detected = detect_llm_config()

    use_llm = ask_yes_no(
        "Do you want to use LLM for enhanced analysis? (Required for standard/deep mode)",
        True,
    )

    if not use_llm:
        print("LLM will not be used. Only fast mode will be available.")
        return {"use_llm": False}

    print("\nLLM configuration (for standard/deep mode):")

    # API Key
    if detected["api_key"]:
        print(
            f"Detected API key: {detected['api_key'][:8]}...{detected['api_key'][-4:]}"
        )
        use_detected = ask_yes_no("Use detected API key?", True)
        if use_detected:
            api_key = detected["api_key"]
        else:
            api_key = ask_input("Enter LLM API key", "")
    else:
        api_key = ask_input("Enter LLM API key", "")

    if not api_key:
        print("API key is required for LLM usage.")
        if ask_yes_no("Skip LLM configuration?", True):
            return {"use_llm": False}
        else:
            api_key = ask_input("Enter LLM API key (required)", "")

    # Base URL
    default_base_url = detected["base_url"] or "https://api.openai.com/v1"
    base_url = ask_input("Enter LLM base URL", default_base_url)

    # Model
    default_model = detected["model"] or "gpt-4o"
    model = ask_input("Enter LLM model", default_model)

    # Test configuration
    if ask_yes_no("Test LLM connection?", True):
        if test_llm_connection(api_key, base_url, model):
            print("✓ LLM connection test successful")
        else:
            print("✗ LLM connection test failed")
            if not ask_yes_no("Continue anyway?", False):
                return {"use_llm": False}

    return {
        "use_llm": True,
        "llm_api_key": api_key,
        "llm_base_url": base_url,
        "llm_model": model,
    }


def test_llm_connection(api_key: str, base_url: str, model: str) -> bool:
    """Test LLM connection."""
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        # Simple test call
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5,
        )

        return response.choices[0].message.content is not None
    except Exception as e:
        print(f"Error testing LLM: {e}")
        return False


def setup_output_config():
    """Setup output configuration."""
    print_step(4, 4, "Configuring output settings")

    default_output_dir = str(Path.home() / "math_paper_analysis")
    output_dir = ask_input("Enter default output directory", default_output_dir)

    # Create directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True, parents=True)

    auto_open = ask_yes_no("Open analysis results automatically?", True)

    return {
        "output_dir": output_dir,
        "auto_open_results": auto_open,
    }


def create_analyzer_script(config: Dict, script_path: Path):
    """Create a ready-to-use analyzer script."""
    template = '''#!/usr/bin/env python3
"""Math Paper Analyzer - Ready to use!"""

import os
import sys
from pathlib import Path

# Add script directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from scripts.paper_analyzer import MathPaperAnalyzer


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python {} <pdf_file> [mode]".format(Path(__file__).name))
        print("Modes: fast, standard, deep (default: standard)")
        print("Example: python {} paper.pdf deep".format(Path(__file__).name))
        return 1
    
    pdf_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "standard"
    
    if mode not in ["fast", "standard", "deep"]:
        print(f"Invalid mode: {mode}. Use fast, standard, or deep.")
        return 1
    
    # Load configuration
    config_path = script_dir / "config.json"
    if not config_path.exists():
        print("Configuration not found. Please run setup first.")
        return 1
    
    import json
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Create analyzer
    analyzer = MathPaperAnalyzer(
        ocr_url=config.get("ocr_url", "https://edusys5.sii.edu.cn/ocr"),
        llm_api_key=config.get("llm_api_key") if config.get("use_llm", False) else None,
        llm_base_url=config.get("llm_base_url"),
        llm_model=config.get("llm_model", "gpt-4o"),
    )
    
    # Check mode availability
    if mode in ["standard", "deep"] and not config.get("use_llm", False):
        print(f"LLM is not configured. {mode} mode requires LLM.")
        print("Using fast mode instead.")
        mode = "fast"
    
    # Analyze paper
    output_dir = config.get("output_dir", str(Path(pdf_path).parent))
    results = analyzer.analyze_paper(
        pdf_path=pdf_path,
        mode=mode,
        save_output=True,
        output_dir=output_dir,
    )
    
    # Show results
    if results.get("errors"):
        print("\nErrors occurred:")
        for error in results["errors"]:
            print(f"  - {error}")
    
    print("\n" + "=" * 60)
    print("Analysis completed!")
    
    # Show output files
    if "output" in results:
        paper_name = Path(pdf_path).stem
        output_path = Path(output_dir)
        
        print(f"\nOutput files in {output_path}:")
        report_file = output_path / f"{paper_name}_{mode}_analysis.md"
        if report_file.exists():
            print(f"  - {report_file.name} (full report)")
        
        struct_file = output_path / f"{paper_name}_structure.md"
        if struct_file.exists():
            print(f"  - {struct_file.name} (structure only)")
        
        if mode == "deep":
            summary_file = output_path / f"{paper_name}_summary.md"
            if summary_file.exists():
                print(f"  - {summary_file.name} (summary only)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(template)

    # Make executable
    script_path.chmod(0o755)
    print(f"✓ Created analyzer script: {script_path}")


def main():
    """Main setup function."""
    print_header("Math Paper Analyzer Setup Wizard")

    # Get script directory
    script_dir = Path(__file__).parent.parent
    config_path = script_dir / "config.json"

    # Check if already configured
    if config_path.exists():
        print("Existing configuration found.")
        if not ask_yes_no("Do you want to reconfigure?", False):
            print("Using existing configuration.")
            return 0

    # Run setup steps
    if not setup_dependencies():
        return 1

    config = {}
    config.update(setup_ocr_config())
    config.update(setup_llm_config())
    config.update(setup_output_config())

    # Save configuration
    save_config(config, config_path)

    # Create ready-to-use script
    analyzer_script = script_dir / "analyze_paper.py"
    create_analyzer_script(config, analyzer_script)

    print_header("Setup Complete!")

    print("\n🎉 Math Paper Analyzer is ready to use!")
    print("\nQuick start:")
    print(f"  1. Analyze a paper: python {analyzer_script.name} paper.pdf")
    print(f"  2. Use deep mode: python {analyzer_script.name} paper.pdf deep")
    print(f"  3. Use fast mode: python {analyzer_script.name} paper.pdf fast")

    print("\nConfiguration saved to:")
    print(f"  - {config_path}")
    print(f"  - You can edit this file to change settings")

    print("\nNext steps:")
    print("  1. Try analyzing a sample paper")
    print("  2. Check the output directory:", config.get("output_dir", "Not set"))
    print("  3. Refer to README.md for more information")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(1)
