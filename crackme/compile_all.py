import shutil
import subprocess
import sys

from helpers import binary_dir, root

shutil.rmtree(binary_dir, ignore_errors=True)
(binary_dir / "train").mkdir(parents=True, exist_ok=True)
(binary_dir / "valid").mkdir(parents=True, exist_ok=True)
(binary_dir / "train" / "answer.json").write_text("{}\n", encoding="utf-8")
(binary_dir / "valid" / "answer.json").write_text("{}\n", encoding="utf-8")

for i in range(1, 8):
    subprocess.run([sys.executable, "compile.py"], cwd=root / str(i), check=True)

for i in range(1, 8):
    for obj in (root / str(i)).glob("*.obj"):
        obj.unlink(missing_ok=True)
