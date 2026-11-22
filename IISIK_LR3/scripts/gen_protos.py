from __future__ import annotations

import sys
from pathlib import Path

from grpc_tools import protoc

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
PROTOS_DIR = ROOT / "protos"
OUT_DIR = ROOT / "shared" / "protogen"
WELL_KNOWN = Path(protoc.__file__).resolve().parent / "_proto"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    proto_files = sorted(str(path) for path in PROTOS_DIR.glob("*.proto"))
    args = [
        "grpc_tools.protoc",
        f"-I{PROTOS_DIR}",
        f"-I{WELL_KNOWN}",
        f"--python_out={OUT_DIR}",
        f"--grpc_python_out={OUT_DIR}",
        *proto_files,
    ]
    code = protoc.main(args)
    if code != 0:
        return code
    for generated in OUT_DIR.glob("*_pb2*.py"):
        lines = generated.read_text(encoding="utf-8").splitlines(keepends=True)
        generated.write_text(
            "".join(line for line in lines if not line.startswith("#")),
            encoding="utf-8",
            newline="",
        )
    (OUT_DIR / "__init__.py").write_text(
        "from __future__ import annotations\n\n"
        "import sys\n"
        "from pathlib import Path\n\n"
        "_DIR = str(Path(__file__).resolve().parent)\n"
        "if _DIR not in sys.path:\n"
        "    sys.path.append(_DIR)\n",
        encoding="utf-8",
    )
    print(f"Сгенерировано {len(proto_files)} контрактов в {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
