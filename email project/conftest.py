"""
WHY THIS FILE IS IMPORTANT:
---------------------------
When running `pytest` from the terminal, Python looks for imported modules (like `prompt_library` 
or `email_generator`) inside the `tests/` directory by default.

This `conftest.py` file is automatically executed by pytest before running any tests.
It adds the root project directory to Python's module search path (`sys.path`).

Without this file, running `pytest` will result in a `ModuleNotFoundError` when test files 
try to import modules located at the project root.
"""

import sys
import os

# Add project root directory to sys.path so tests in tests/ can import project modules
sys.path.insert(0, os.path.dirname(__file__))
