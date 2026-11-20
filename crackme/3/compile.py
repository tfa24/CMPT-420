import json
import random
import string
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from helpers import compile_cpp

cpp_files = ["easy.cpp", "medium.cpp", "hard.cpp", "extreme.cpp"]
output_root = Path("../binary")
all_answers = {"train": {}, "valid": {}}

for split, count in (("train", 3), ("valid", 1)):
    out_dir = output_root / split / "3"
    out_dir.mkdir(parents=True, exist_ok=True)

    for cpp in cpp_files:
        level = cpp[:-4]
        template = Path(cpp).read_text(encoding="utf-8")
        for i in range(1, count + 1):
            max_mask = random.randint(1, 20)
            alphabet = string.ascii_lowercase[max_mask:]
            length = random.randint(10, 30)
            answer = "".join(random.choice(alphabet) for _ in range(length))
            mask = [random.randint(0, max_mask) for _ in range(length + 1)]
            stored = "".join(chr(ord(c) - m) for c, m in zip(answer, mask[:length]))
            mask_init = ", ".join(str(v) for v in mask)

            source = template
            source = source.replace(
                "#define CORRECT_LEN 0", f"#define CORRECT_LEN {length}"
            )
            source = source.replace('#define ANSWER ""', f'#define ANSWER "{stored}"')
            source = source.replace(
                "char mask[CORRECT_LEN + 1] = {0};",
                f"char mask[CORRECT_LEN + 1] = {{{mask_init}}};",
            )

            Path(cpp).write_text(source, encoding="utf-8")
            try:
                compile_cpp(Path(cpp), out_dir / f"{level}_{i}")
            finally:
                Path(cpp).write_text(template, encoding="utf-8")
            all_answers[split][f"{level}_{i}"] = answer

for split in ("train", "valid"):
    answer_path = output_root / split / "answer.json"
    data = json.loads(answer_path.read_text(encoding="utf-8"))
    data["3"] = all_answers[split]
    answer_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
