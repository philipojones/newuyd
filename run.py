#!/usr/bin/env python3
"""
UYD Website & API Server Startup
Runs both the website and API on the same port
"""

import subprocess
import sys
import os
from pathlib import Path

def run_server():
    """Run the FastAPI server with templates and static files"""
    print("Starting United Youth Developers Server...")
    print("Website & API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("=" * 60)

    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    try:
        # Run uvicorn with auto-reload
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ]

        subprocess.run(cmd, check=True)

    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_server()
