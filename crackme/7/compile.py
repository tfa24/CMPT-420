import json
import random
import string
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from helpers import compile_cpp

cpp_files = ["easy.cpp", "medium.cpp", "hard.cpp", "extreme.cpp"]
alphabet = string.ascii_letters + string.digits
output_root = Path("../binary")
all_answers = {"train": {}, "valid": {}}

for split, count in (("train", 3), ("valid", 1)):
    out_dir = output_root / split / "7"
    out_dir.mkdir(parents=True, exist_ok=True)

    for cpp in cpp_files:
        level = cpp[:-4]
        template = Path(cpp).read_text(encoding="utf-8")
        for i in range(1, count + 1):
            length = random.randint(10, 30)
            password = "".join(random.choice(alphabet) for _ in range(length))
            hour_start = random.randint(0, 23)
            hour_end = random.randint(hour_start, 23)

            source = template
            source = source.replace("#define PASSLEN 0", f"#define PASSLEN {length}")
            source = source.replace(
                "#define HOUR_START 0", f"#define HOUR_START {hour_start}"
            )
            source = source.replace(
                "#define HOUR_END 0", f"#define HOUR_END {hour_end}"
            )
            source = source.replace('#define ANSWER ""', f'#define ANSWER "{password}"')

            Path(cpp).write_text(source, encoding="utf-8")
            try:
                compile_cpp(Path(cpp), out_dir / f"{level}_{i}")
            finally:
                Path(cpp).write_text(template, encoding="utf-8")
            all_answers[split][f"{level}_{i}"] = {
                "password": password,
                "hour_start": hour_start,
                "hour_end": hour_end,
            }

for split in ("train", "valid"):
    answer_path = output_root / split / "answer.json"
    data = json.loads(answer_path.read_text(encoding="utf-8"))
    data["7"] = all_answers[split]
    answer_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
