import subprocess
import sys

try:
    # Add all changes
    subprocess.run(["git", "add", "."], check=True)

    # Commit
    message = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Update"
    )
    subprocess.run(
        ["git", "commit", "-m", message],
        check=True
    )

    # Push
    subprocess.run(
        ["git", "push"],
        check=True
    )

    print("✅ Git push completed successfully.")

except subprocess.CalledProcessError as e:
    print(f"❌ Git command failed: {e}")