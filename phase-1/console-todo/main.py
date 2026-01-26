#!/usr/bin/env python3
"""Main entry point for Todo Application.

Evolution of Todo - Phase I: In-Memory Python Console App

Run with: cd phase-1/console-todo && python main.py

Per Constitution Principle I: Spec-Driven Development
All features implemented according to specifications in /specs_history/phase_1/
"""

import sys
import os

# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.menu import run


def main() -> None:
    """Application entry point."""
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
