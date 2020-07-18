import argparse
import subprocess
import os

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), ".."))
build_ = os.path.join(root_dir, "_internal", "build.py")
clean_ = os.path.join(root_dir, "_internal", "clean.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a website from files discovered under source/"
    )

    parser.add_argument('target', help="The target scrapwiki command.")
    parser.add_argument('--clean', dest="clean", action='store_true', default=False)
    args = parser.parse_args()

    if args.target == "build":
      if args.clean:
        subprocess.check_call(["python", clean_])

      subprocess.check_call(["python", build_])
    else:
      print("Not a recognized command. Exiting.")





