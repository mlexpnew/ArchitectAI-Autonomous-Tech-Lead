"""
AI Model Generator
"""

from pathlib import Path

from core.project_context import ProjectContext
from generators.ai.code_generator import AICodeGenerator
from generators.writer import FileWriter
from quality.quality_controller import QualityController
from review.code_fixer import CodeFixer
from review.code_reviewer import CodeReviewer
from validation.python_validator import PythonValidator


class AIModelGenerator:

    def __init__(
        self,
        output_dir: str,
    ):
        self.output_dir = Path(output_dir)
        self.ai = AICodeGenerator()
        self.reviewer = CodeReviewer()
        self.fixer = CodeFixer()
        self.validator = PythonValidator()
        self.quality = QualityController()

    def generate(
        self,
        entity_name: str,
        fields: list[str],
    ):
        prompt = f"""
Generate a production-ready SQLAlchemy 2.0 model.

Entity:
{entity_name}

Fields:
{chr(10).join(fields)}

Requirements

- SQLAlchemy 2.0
- DeclarativeBase
- Python 3.12
- Type hints
- Relationships if applicable
- Clean Architecture
- Return ONLY Python code.
"""

        # Build Project Context
        context = ProjectContext(
            self.output_dir,
        ).build_for_entity(
            entity_name,
        )

        # Generate Code
        code = self.ai.generate(
            prompt=prompt,
            project_context=context,
        )

        print("\n" + "=" * 80)
        print("RAW GENERATED CODE")
        print("=" * 80)
        print(code)
        print("=" * 80)

        # AI Review
        code = self.reviewer.review(code)

        print("\n" + "=" * 80)
        print("AFTER REVIEW")
        print("=" * 80)
        print(code)
        print("=" * 80)

        # Syntax Validation + Auto Fix
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            valid, error = self.validator.validate(code)
            if valid:
                break

            print(f"\n⚠️ Syntax Error (Attempt {attempt + 1})")
            print(error)

            code = self.fixer.fix(code, error)
        else:
            raise RuntimeError(f"Generated code is still invalid:\n{error}")

        # AI Quality Improvement
        print("\n⭐ Running Quality Controller...")
        code = self.quality.improve(code)

        # Final Validation
        valid, error = self.validator.validate(code)
        if not valid:
            raise RuntimeError(f"Quality Controller returned invalid code:\n{error}")

        # Save File
        output_file = (
            self.output_dir
            / "backend"
            / "app"
            / "models"
            / f"{entity_name.lower()}.py"
        )

        FileWriter.write(output_file, code)
        print(f"✅ Generated {entity_name} model")
        return output_file