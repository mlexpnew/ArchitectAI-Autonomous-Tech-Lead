"""
Router Generator

Generates the application's main.py
"""

from pathlib import Path

from generators.writer import FileWriter


class RouterGenerator:

    def __init__(
        self,
        output_dir,
    ):
        self.output_dir = Path(output_dir)

    def generate(
        self,
        entities,
    ):

        router_imports = []
        router_includes = []

        model_imports = []

        for entity in entities:

            lower = entity.name.lower()

            router_imports.append(
                f"from app.api import {lower}"
            )

            model_imports.append(
                f"from app.models.{lower} import {entity.name}"
            )

            router_includes.append(
                f"app.include_router({lower}.router)"
            )

        code = f'''"""
Generated FastAPI Application
"""

from fastapi import FastAPI

from app.database import Base
from app.database import engine

{chr(10).join(model_imports)}

{chr(10).join(router_imports)}

app = FastAPI(
    title="Generated API",
    version="1.0.0",
)

# ----------------------------------------
# Create database tables automatically
# ----------------------------------------

Base.metadata.create_all(bind=engine)

# ----------------------------------------
# Register Routers
# ----------------------------------------

{chr(10).join(router_includes)}

@app.get("/")
def root():

    return {{
        "status": "running",
        "message": "API Generated Successfully"
    }}
'''

        FileWriter.write(
            self.output_dir
            / "backend"
            / "app"
            / "main.py",
            code,
        )

        print("✅ Generated main.py")