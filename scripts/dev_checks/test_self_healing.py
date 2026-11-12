#cd /Users/chandini/ArchitectAI-Autonomous-Tech-Lead

#cat > test_self_healing.py <<'PY'
"""
ArchitectAI Self-Healing Integration Test

Flow:
1. Verify generated backend is healthy.
2. Intentionally break an existing generated API file.
3. Verify validation detects the failure.
4. Run SelfHealingEngine.
5. Verify the backend becomes healthy again.
6. Restore the original file if anything goes wrong.
"""

from pathlib import Path
import shutil

from orchestration.project_validator import ProjectValidator
from orchestration.self_healing_engine import SelfHealingEngine


BACKEND_DIR = Path(
    "generated_projects/Library_System/backend"
).resolve()

TARGET_FILE = (
    BACKEND_DIR
    / "app"
    / "api"
    / "book.py"
)

SAFETY_BACKUP = TARGET_FILE.with_suffix(
    ".py.integration_test_backup"
)


def validate_backend():
    validator = ProjectValidator(
        backend_dir=str(BACKEND_DIR)
    )

    return validator.validate()


def main():

    print("\n" + "=" * 70)
    print("🧪 ARCHITECTAI SELF-HEALING INTEGRATION TEST")
    print("=" * 70)

    if not BACKEND_DIR.exists():
        raise RuntimeError(
            f"Backend does not exist: {BACKEND_DIR}"
        )

    if not TARGET_FILE.exists():
        raise RuntimeError(
            f"Target file does not exist: {TARGET_FILE}"
        )

    # ---------------------------------------------------------
    # Step 1: Verify healthy baseline
    # ---------------------------------------------------------

    print(
        "\n[1/5] 🔍 Checking healthy baseline..."
    )

    baseline = validate_backend()

    if not baseline["valid"]:
        raise RuntimeError(
            "Library backend must be healthy "
            "before running this test."
        )

    print(
        "✅ Baseline project is healthy"
    )

    # ---------------------------------------------------------
    # Step 2: Safety backup
    # ---------------------------------------------------------

    shutil.copy2(
        TARGET_FILE,
        SAFETY_BACKUP,
    )

    print(
        f"✅ Safety backup created: "
        f"{SAFETY_BACKUP.name}"
    )

    try:

        # -----------------------------------------------------
        # Step 3: Introduce controlled syntax failure
        # -----------------------------------------------------

        print(
            "\n[2/5] 💥 Introducing controlled failure..."
        )

        original_code = TARGET_FILE.read_text(
            encoding="utf-8"
        )

        broken_code = (
            original_code
            + "\n\n"
            + "def architectai_intentional_failure(\n"
        )

        TARGET_FILE.write_text(
            broken_code,
            encoding="utf-8",
        )

        print(
            f"💥 Intentionally broke: "
            f"{TARGET_FILE.relative_to(BACKEND_DIR)}"
        )

        # -----------------------------------------------------
        # Step 4: Ensure validator detects it
        # -----------------------------------------------------

        print(
            "\n[3/5] 🔍 Confirming failure detection..."
        )

        broken_validation = validate_backend()

        if broken_validation["valid"]:
            raise RuntimeError(
                "Validator failed to detect the "
                "intentional syntax error."
            )

        print(
            "✅ Validator detected the broken project"
        )

        # -----------------------------------------------------
        # Step 5: Run autonomous self-healing
        # -----------------------------------------------------

        print(
            "\n[4/5] 🧠 Running SelfHealingEngine..."
        )

        healer = SelfHealingEngine(
            backend_dir=str(BACKEND_DIR),
            max_attempts=2,
        )

        healing_result = healer.heal()

        print(
            "\nHealing result:"
        )

        print(
            f" - Healed: "
            f"{healing_result['healed']}"
        )

        print(
            f" - Attempts: "
            f"{healing_result['attempts']}"
        )

        if not healing_result["healed"]:
            raise RuntimeError(
                "Self-healing engine could not "
                "repair the generated backend."
            )

        # -----------------------------------------------------
        # Final validation
        # -----------------------------------------------------

        print(
            "\n[5/5] 🧪 Running final validation..."
        )

        final_validation = validate_backend()

        if not final_validation["valid"]:
            raise RuntimeError(
                "Backend is still invalid after healing."
            )

        print(
            "\n" + "=" * 70
        )

        print(
            "🎉 SELF-HEALING INTEGRATION TEST PASSED"
        )

        print(
            "=" * 70
        )

    finally:

        # -----------------------------------------------------
        # Absolute safety restore
        # -----------------------------------------------------
        #
        # We restore the original generated file after this
        # integration test so the Library project remains
        # deterministic regardless of the AI-generated repair.
        # -----------------------------------------------------

        if SAFETY_BACKUP.exists():

            shutil.copy2(
                SAFETY_BACKUP,
                TARGET_FILE,
            )

            SAFETY_BACKUP.unlink()

            print(
                "\n↩️ Integration-test target restored "
                "to original state."
            )

        # Remove any internal repair backup left behind.
        repair_backup = TARGET_FILE.with_suffix(
            ".py.bak"
        )

        repair_backup.unlink(
            missing_ok=True
        )


if __name__ == "__main__":
    main()