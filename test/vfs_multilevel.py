import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: test path/to/root/of/the/project")
    exit(1)

root_dir = sys.argv[1]

print(f">> testing \"python {root_dir}/main.py\" {root_dir}/test/vfs_multilevel.xml {root_dir}/test/.sheshrc")
test2_output = subprocess.check_output(
    ["python", f"{root_dir}/main.py", f"{root_dir}/test/vfs_multilevel.xml",
     f"{root_dir}/test/.multilevel_sheshrc"]
)
print(test2_output.decode())
