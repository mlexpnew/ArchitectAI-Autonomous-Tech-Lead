"""
Main FastAPI Generator
"""

from pathlib import Path

from generators.writer import FileWriter


class MainGenerator:

    def __init__(self, output_dir):

        self.output_dir = Path(output_dir)

    def generate(self):

        code = '''"""
Application Entry Point
"""

from fastapi import FastAPI

app = FastAPI(
    title="Generated API",
    version="1.0.0",
)


@app.get("/")
def health():

    return {
        "status": "healthy",
    }
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "main.py",
            code,
        )

        print("✅ main.py")