import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
binary_dir = root / "binary"
cloakwork_dir = root / "Cloakwork"


def compile_cpp(source: Path, output: Path):
    subprocess.run(
        [
            "cl",
            "/nologo",
            "/std:c++20",
            "/EHsc",
            "/O2",
            f"/I{cloakwork_dir}",
            str(source),
            f"/Fe{output}",
            "/link",
            "/MACHINE:X64",
        ],
        cwd=source.parent,
        check=True,
    )
