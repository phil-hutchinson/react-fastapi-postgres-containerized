import sys
import os

# Ensure the backend root is on the Python path so 'api' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
