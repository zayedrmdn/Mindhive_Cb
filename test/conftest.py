# test/conftest.py
import sys, os

# ensure project root is on sys.path so `import app…` works
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
