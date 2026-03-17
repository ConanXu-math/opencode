#!/usr/bin/env python3
"""Auto-configured math paper analyzer with intelligent setup."""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any


class AutoMathPaperAnalyzer:
    """Auto-configured analyzer with intelligent setup."""

    def __init__(self):
        self.script_dir = Path(__file__).parent.parent
        self.config_path = self.script_dir / "config.json"
        self.config = self._load_or_create_config()

    def _load_or_create_config(self) -> Dict[str, Any]:
        """Load existing config or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️  Configuration file corrupted, creating new one.")

        # Default configuration
        return {
            "ocr_url": "https://edusys5.sii.edu.cn/ocr",
            "use_llm": False,
            "output_dir": str(Path.home() / "math_paper_analysis"),
            "auto_setup_done": False,
        }

    def _check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        required_packages = [
            ("pymupdf", "fitz"),
            ("httpx", "httpx"),
        ]

        missing = []
        for package, import_name in required_packages:
            try:
                __import__(import_name)
            except ImportError:
                missing.append(package)

        if missing:
            print(f"⚠️  Missing dependencies: {', '.join(missing)}")
            return False

        return True

    def _install_dependencies(self) -> bool:
        """Install missing dependencies automatically."""
        print("Installing required dependencies...")

        packages = ["pymupdf", "httpx"]
        for package in packages:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print(f"✓ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"✗ Failed to install {package}")
                return False

        return True

    def _detect_llm_config(self) -> Dict[str, Optional[str]]:
        """Detect LLM configuration from environment."""
        config = {
            "api_key": None,
            "base_url": None,
            "model": None,
        }

        # Check common environment variables
        env_mapping = {
            "api_key": ["OPENAI_API_KEY", "LLM_API_KEY"],
            "base_url": ["OPENAI_BASE_URL", "LLM_BASE_URL"],
            "model": ["OPENAI_MODEL", "LLM_MODEL_ID"],
        }

        for key, var_names in env_mapping.items():
            for var_name in var_names:
                value = os.getenv(var_name)
                if value:
                    config[key] = value
                    break

        return config

    def _test_llm_connection(self, api_key: str, base_url: str, model: str) -> bool:
        """Test LLM connection."""
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=api_key,
                base_url=base_url,
            )

            # Quick test
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
            )

            return response.choices[0].message.content is not None
        except Exception:
            return False

    def _auto_configure_llm(self) -> bool:
        """Auto-configure LLM if possible."""
        detected = self._detect_llm_config()

        if not detected["api_key"]:
            print("ℹ️  No LLM API key detected in environment variables.")
            print("   Only fast mode will be available.")
            return False

        # Test the detected configuration
        print("Testing detected LLM configuration...")
        if self._test_llm_connection(
            detected["api_key"],
            detected["base_url"] or "https://api.openai.com/v1",
            detected["model"] or "gpt-4o",
        ):
            print("✓ LLM configuration detected and working")
            self.config.update(
                {
                    "use_llm": True,
                    "llm_api_key": detected["api_key"],
                    "llm_base_url": detected["base_url"] or "https://api.openai.com/v1",
                    "llm_model": detected["model"] or "gpt-4o",
                }
            )
            return True
        else:
            print("⚠️  LLM configuration detected but connection failed")
            return False

    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        output_dir = self.config.get(
            "output_dir", str(Path.home() / "math_paper_analysis")
        )
        Path(output_dir).mkdir(exist_ok=True, parents=True)

    def _save_config(self):
        """Save configuration."""
        self.config["auto_setup_done"] = True
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def setup(self, interactive: bool = False) -> bool:
        """Setup the analyzer automatically."""
        print("🔧 Setting up Math Paper Analyzer...")

        # Check and install dependencies
        if not self._check_dependencies():
            print("Installing missing dependencies...")
            if not self._install_dependencies():
                print("Failed to install dependencies. Please install manually:")
                print("  pip install pymupdf httpx")
                if interactive:
                    input("Press Enter to continue with limited functionality...")
                else:
                    return False

        # Auto-configure LLM
        llm_configured = self._auto_configure_llm()

        if interactive and not llm_configured:
            print("\nLLM is required for standard and deep analysis modes.")
            response = (
                input("Do you want to configure LLM now? [y/N]: ").strip().lower()
            )
            if response in ["y", "yes"]:
                # Run interactive setup
                from interactive_setup import setup_llm_config

                llm_config = setup_llm_config()
                self.config.update(llm_config)
                llm_configured = llm_config.get("use_llm", False)

        # Ensure output directory
        self._ensure_output_dir()

        # Save configuration
        self._save_config()

        print("\n✅ Setup complete!")
        if llm_configured:
            print("   LLM configured: Standard and deep modes available")
        else:
            print("   LLM not configured: Only fast mode available")

        print(f"   Output directory: {self.config.get('output_dir')}")

        return True

    def analyze(self, pdf_path: str, mode: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a paper with automatic configuration."""
        # Check if setup is needed
        if not self.config.get("auto_setup_done", False):
            print("First-time setup required...")
            if not self.setup(interactive=True):
                return {"error": "Setup failed"}

        # Validate PDF path
        pdf_path_obj = Path(pdf_path)
        if not pdf_path_obj.exists():
            return {"error": f"PDF file not found: {pdf_path}"}

        # Determine mode
        if not mode:
            if self.config.get("use_llm", False):
                mode = "standard"
            else:
                mode = "fast"
                print("ℹ️  LLM not configured, using fast mode")

        # Validate mode
        if mode not in ["fast", "standard", "deep"]:
            return {"error": f"Invalid mode: {mode}. Use fast, standard, or deep."}

        # Check mode availability
        if mode in ["standard", "deep"] and not self.config.get("use_llm", False):
            print(f"⚠️  {mode} mode requires LLM. Using fast mode instead.")
            mode = "fast"

        # Import analyzer (delayed import to avoid dependency issues)
        try:
            from paper_analyzer import MathPaperAnalyzer
        except ImportError as e:
            return {"error": f"Failed to import analyzer: {e}"}

        # Create analyzer
        analyzer = MathPaperAnalyzer(
            ocr_url=self.config.get("ocr_url", "https://edusys5.sii.edu.cn/ocr"),
            llm_api_key=self.config.get("llm_api_key")
            if self.config.get("use_llm", False)
            else None,
            llm_base_url=self.config.get("llm_base_url"),
            llm_model=self.config.get("llm_model", "gpt-4o"),
        )

        # Analyze paper
        print(f"\n📄 Analyzing: {pdf_path_obj.name}")
        print(f"🔍 Mode: {mode}")

        try:
            results = analyzer.analyze_paper(
                pdf_path=str(pdf_path_obj),
                mode=mode,
                save_output=True,
                output_dir=self.config.get("output_dir"),
            )

            # Add analysis info
            results["analysis_info"] = {
                "paper": pdf_path_obj.name,
                "mode": mode,
                "llm_available": self.config.get("use_llm", False),
            }

            return results

        except Exception as e:
            return {"error": f"Analysis failed: {e}"}

    def get_status(self) -> Dict[str, Any]:
        """Get analyzer status."""
        return {
            "configured": self.config.get("auto_setup_done", False),
            "llm_available": self.config.get("use_llm", False),
            "output_dir": self.config.get("output_dir"),
            "ocr_url": self.config.get("ocr_url"),
        }


def main():
    """Command-line interface."""
    if len(sys.argv) < 2:
        print("Usage: python auto_analyzer.py <pdf_file> [mode]")
        print("Modes: fast, standard, deep (auto-detected if not specified)")
        print("Example: python auto_analyzer.py paper.pdf")
        print("         python auto_analyzer.py paper.pdf deep")
        return 1

    pdf_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else None

    # Create and run analyzer
    analyzer = AutoMathPaperAnalyzer()

    # Analyze paper
    results = analyzer.analyze(pdf_path, mode)

    # Handle results
    if "error" in results:
        print(f"\n❌ Error: {results['error']}")
        return 1

    # Show success message
    print("\n✅ Analysis completed successfully!")

    # Show output files
    if "output" in results:
        paper_name = Path(pdf_path).stem
        output_dir = analyzer.config.get("output_dir", str(Path(pdf_path).parent))
        output_path = Path(output_dir)

        print(f"\n📁 Output files in {output_path}:")

        mode_used = results.get("analysis_info", {}).get("mode", "unknown")
        report_file = output_path / f"{paper_name}_{mode_used}_analysis.md"
        if report_file.exists():
            print(f"  📄 {report_file.name} (full report)")

        struct_file = output_path / f"{paper_name}_structure.md"
        if struct_file.exists():
            print(f"  📊 {struct_file.name} (structure only)")

        if mode_used == "deep":
            summary_file = output_path / f"{paper_name}_summary.md"
            if summary_file.exists():
                print(f"  📝 {summary_file.name} (summary only)")

    # Show timing if available
    if "timing" in results:
        print(f"\n⏱️  Timing:")
        for stage, time in results["timing"].items():
            print(f"  {stage:12}: {time:.1f}s")

    return 0


if __name__ == "__main__":
    sys.exit(main())
