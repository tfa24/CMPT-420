import json
import random
import string
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from helpers import compile_cpp

cpp_files = ["easy.cpp", "medium.cpp", "hard.cpp", "extreme.cpp"]
output_root = Path("../binary")
alphabet = string.ascii_letters + string.digits
all_answers = {"train": {}, "valid": {}}

for split, count in (("train", 3), ("valid", 1)):
    out_dir = output_root / split / "5"
    out_dir.mkdir(parents=True, exist_ok=True)

    for cpp in cpp_files:
        level = cpp[:-4]
        template = Path(cpp).read_text(encoding="utf-8")
        for i in range(1, count + 1):
            fixed_a, fixed_b = random.sample(range(16), 2)
            fixed_char_a = random.choice(alphabet)
            fixed_char_b = random.choice(alphabet)
            mods = [random.randint(2, 9) for _ in range(4)]

            source = template
            source = source.replace(
                "#define FIXED_INDEX_A 0", f"#define FIXED_INDEX_A {fixed_a}"
            )
            source = source.replace(
                "#define FIXED_CHAR_A 0", f"#define FIXED_CHAR_A '{fixed_char_a}'"
            )
            source = source.replace(
                "#define FIXED_INDEX_B 0", f"#define FIXED_INDEX_B {fixed_b}"
            )
            source = source.replace(
                "#define FIXED_CHAR_B 0", f"#define FIXED_CHAR_B '{fixed_char_b}'"
            )
            source = source.replace("#define MOD_0 0", f"#define MOD_0 {mods[0]}")
            source = source.replace("#define MOD_1 0", f"#define MOD_1 {mods[1]}")
            source = source.replace("#define MOD_2 0", f"#define MOD_2 {mods[2]}")
            source = source.replace("#define MOD_3 0", f"#define MOD_3 {mods[3]}")

            Path(cpp).write_text(source, encoding="utf-8")
            try:
                compile_cpp(Path(cpp), out_dir / f"{level}_{i}")
            finally:
                Path(cpp).write_text(template, encoding="utf-8")
            all_answers[split][f"{level}_{i}"] = {
                "len": 16,
                "block_size": 4,
                "fixed_index_a": fixed_a,
                "fixed_char_a": fixed_char_a,
                "fixed_index_b": fixed_b,
                "fixed_char_b": fixed_char_b,
                "mods": mods,
            }

for split in ("train", "valid"):
    answer_path = output_root / split / "answer.json"
    data = json.loads(answer_path.read_text(encoding="utf-8"))
    data["5"] = all_answers[split]
    answer_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
