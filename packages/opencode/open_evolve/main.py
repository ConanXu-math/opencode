#!/usr/bin/env python3
"""
OpenEvolve Python Agent - 统一入口点
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from open_evolve.cli.commands import main as cli_main


def main():
    """主入口点"""
    cli_main()


if __name__ == "__main__":
    main()
