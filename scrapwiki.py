import argparse
import subprocess
import os
import json

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), ".."))
build_ = os.path.join(root_dir, "_internal", "build.py")
target = os.path.join(root_dir, "docs")
internal_dir = os.path.join(root_dir, "_internal")
clean = os.path.join(internal_dir, "clean.py")
config_file = os.path.join(internal_dir, "config.json")

if os.path.exists(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        content = f.read()
        CONFIG = json.loads(content)
else:
    CONFIG = {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a website from files discovered under source/"
    )

    parser.add_argument("target", help="The target scrapwiki command.")
    parser.add_argument("--clean", dest="clean", action="store_true", default=False)
    args = parser.parse_args()

    if args.target == "build":
        if args.clean:
            subprocess.check_call(["python", clean])

        subprocess.check_call(["python", build_])
    elif args.target == "serve":
        # poller implementation
        subprocess.check_call(["python", build_])
        target_port = CONFIG.get("serve_port", "8000")
        print(target_port)

        subprocess.check_call(["python", "-m", "http.server", target_port], cwd = target)
    else:
        print("Not a recognized command. Exiting.")
