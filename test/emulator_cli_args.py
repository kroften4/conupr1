import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: test path/to/root/of/the/project")
    exit(1)

root_dir = sys.argv[1]

print(f">> testing \"python {root_dir}/main.py\" (no arguments)")
try:
    test2_output = subprocess.check_output(
        ["python", f"{root_dir}/main.py"]
    )
except subprocess.CalledProcessError as exc:
    test2_output = exc.output
    print(">> emulator returned an error")
print(test2_output.decode())

print()

print(f">> testing \"python {root_dir}/main.py dummy/path/to/vfs {root_dir}/test/.non_existent_file\" (incorrect path)")
try:
    test2_output = subprocess.check_output(
        ["python", f"{root_dir}/main.py", "dummy/path/to/vfs", f"{root_dir}/test/.non_existent_file"]
    )
except subprocess.CalledProcessError as exc:
    test2_output = exc.output
    print(">> emulator returned an error")
print(test2_output.decode())

print()

print(f">> testing \"python {root_dir}/main.py {root_dir}/test/vfs_minimal.xml {root_dir}/test/.sheshrc\" (correct path)")
test2_output = subprocess.check_output(
    ["python", f"{root_dir}/main.py", f"{root_dir}/test/vfs_minimal.xml", f"{root_dir}/test/.sheshrc"]
)
print(test2_output.decode())
