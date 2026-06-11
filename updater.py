import os
import sys
import time
import shutil
import subprocess

APP_NAME = "micsam.exe"
NEW_APP_NAME = "micsam_new.exe"


def main():
    # Wait for main app to fully exit
    time.sleep(1)

    if not os.path.exists(NEW_APP_NAME):
        print(f"{NEW_APP_NAME} not found")
        sys.exit(1)

    try:
        # Remove old executable
        if os.path.exists(APP_NAME):
            os.remove(APP_NAME)

        # Rename downloaded update
        shutil.move(NEW_APP_NAME, APP_NAME)

        # Restart application
        subprocess.Popen([APP_NAME], shell=True)

    except Exception as e:
        print(f"Update failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
