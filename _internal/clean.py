import os, shutil

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", ".."))
target_dir = os.path.join(root_dir, "target")

for filename in os.listdir(target_dir):
    path = os.path.join(target_dir, filename)
    try:
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except Exception as e:
        print("Exception occurred deleting {}. Exception: {}".format(path, e))
