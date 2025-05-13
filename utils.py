import os

def ensure_output_dir():
    os.makedirs("output", exist_ok=True)
