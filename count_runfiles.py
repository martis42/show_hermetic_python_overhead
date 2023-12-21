import os
import subprocess
import sys

print(f"Python version: {sys.version}")

print(f"Our working directory: {os.getcwd()}")

# The working directory is actually one level below the runfiles directory root, as shown by above print statement.
# Thus, we count files and links recursively from our parent directory
subprocess.run(["find ../ -type f,l | wc -l"], shell=True)
