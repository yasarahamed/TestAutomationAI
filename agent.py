import os
import sys
import subprocess
import google.generativeai as genai

# ── Configuration ──────────────────────────────────────────────────────────────

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBCUp3qmTjDD-SBIwH-ktkh2S7aOjUi7aU")
OUTPUT_FILE    = "generated_test.robot"
KEYWORDS_FILE  = "keywords.resource"

# ── Only keyword NAMES are exposed to the agent ────────────────────────────────

KEYWORDS = [
    "Load Tds",
    "Set Pv",
    "Check Cylinder Temperature",
    "Tap Water",
]

SYSTEM_PROMPT = f"""You are a Robot Framework test case generator.

You have access to the following keyword names:
{chr(10).join("- " + k for k in KEYWORDS)}

Rules:
1. Read the user's scenario and select only the keywords they mention or imply.
2. Arrange them in the order that makes sense for the scenario.
3. Generate ONLY the *** Settings *** and *** Test Cases *** sections.
4. In *** Settings ***, import the resource file: Resource    {KEYWORDS_FILE}
5. Give the test case a meaningful name based on the scenario.
6. Add a short comment above the test case explaining what it does.
7. Do NOT include any *** Keywords *** section — definitions are in the resource file.
8. Do NOT invent keywords that are not in the list above.
9. Output ONLY raw Robot Framework code — no explanation, no markdown fences.
"""

# ── Gemini API call ────────────────────────────────────────────────────────────

def generate_test_case(user_prompt: str) -> str:
    """Send user prompt to Gemini and return generated .robot file content."""
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

    print("\n  Sending prompt to Gemini...")
    response = model.generate_content(user_prompt)
    print(response)
    # Strip markdown fences if Gemini wraps the output
    code = response.text.strip()
    if code.startswith("```"):
        lines = code.splitlines()
        code = "\n".join(
            line for line in lines
            if not line.strip().startswith("```")
        ).strip()

    return code


# ── File writer ────────────────────────────────────────────────────────────────

def save_test_file(robot_code: str, filepath: str) -> None:
    with open(filepath, "w") as f:
        f.write(robot_code)
    print(f"  Test file saved → {filepath}")


# ── Robot executor ─────────────────────────────────────────────────────────────

def run_test(filepath: str) -> int:
    print(f"\n  Executing: robot {filepath}\n")
    print("─" * 60)

    result = subprocess.run(["robot", filepath])

    print("─" * 60)
    if result.returncode == 0:
        print("\n  All tests PASSED")
    else:
        print(f"\n  Tests FAILED (exit code {result.returncode})")

    return result.returncode


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("   Robot Framework AI Agent  (powered by Gemini)")
    print("=" * 60)

    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
        print(f"\n  Prompt: {user_prompt}")
    else:
        print("\nAvailable keywords:")
        for kw in KEYWORDS:
            print(f"  • {kw}")
        print()
        user_prompt = input(" Describe your test scenario: ").strip()
        if not user_prompt:
            print("  No prompt provided. Exiting.")
            sys.exit(1)

    # Step 1 — Generate
    robot_code = generate_test_case(user_prompt)

    print("\n  Generated Robot Framework code:")
    print("─" * 60)
    print(robot_code)
    print("─" * 60)

    # Step 2 — Save
    save_test_file(robot_code, OUTPUT_FILE)

    # Step 3 — Execute
    exit_code = run_test(OUTPUT_FILE)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()