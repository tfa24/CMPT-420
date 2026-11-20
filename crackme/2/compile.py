import json
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from helpers import compile_cpp

cpp_files = ["easy.cpp", "medium.cpp", "hard.cpp", "extreme.cpp"]
alphabet = "abcdefghijklmnopqrstuvwxy"
output_root = Path("../binary")
all_answers = {"train": {}, "valid": {}}

for split, count in (("train", 3), ("valid", 1)):
    out_dir = output_root / split / "2"
    out_dir.mkdir(parents=True, exist_ok=True)

    for cpp in cpp_files:
        level = cpp[:-4]
        template = Path(cpp).read_text(encoding="utf-8")
        for i in range(1, count + 1):
            answer = "".join(
                random.choice(alphabet) for _ in range(random.randint(10, 30))
            )
            stored = "".join(chr(ord(c) + 1) for c in answer)
            source = template.replace('#define ANSWER ""', f'#define ANSWER "{stored}"')
            Path(cpp).write_text(source, encoding="utf-8")
            try:
                compile_cpp(Path(cpp), out_dir / f"{level}_{i}")
            finally:
                Path(cpp).write_text(template, encoding="utf-8")
            all_answers[split][f"{level}_{i}"] = answer

for split in ("train", "valid"):
    answer_path = output_root / split / "answer.json"
    data = json.loads(answer_path.read_text(encoding="utf-8"))
    data["2"] = all_answers[split]
    answer_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
