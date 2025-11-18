#!/usr/bin/env python3
"""Generate requirements.txt from pyproject.toml dependencies."""

import tomllib
from pathlib import Path

def generate_requirements():
    """Read pyproject.toml and write requirements.txt."""
    pyproject_path = Path("pyproject.toml")
    requirements_path = Path("requirements.txt")
    
    if not pyproject_path.exists():
        print("Error: pyproject.toml not found")
        return
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    dependencies = data.get("project", {}).get("dependencies", [])
    
    with open(requirements_path, "w") as f:
        for dep in dependencies:
            f.write(f"{dep}\n")
    
    print(f"Generated {requirements_path} with {len(dependencies)} dependencies")

if __name__ == "__main__":
    generate_requirements()