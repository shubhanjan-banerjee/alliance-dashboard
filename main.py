import os
import sys
import subprocess


def main():
    # Launch the Streamlit app
    app_path = os.path.join(os.path.dirname(__file__), "src", "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])


if __name__ == "__main__":
    main()
