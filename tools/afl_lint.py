#!/usr/bin/env python3
import re, sys, pathlib, collections

SRC_DIR = pathlib.Path(__file__).resolve().parents[1] / "src"

VAR_ASSIGN_RX = re.compile(r"(?m)^\s*([A-Za-z_]\w*)\s*=\s*[^=].*;")
FUNC_DEF_RX   = re.compile(r"(?m)^\s*([A-Za-z_]\w*)\s*\(([^)]*)\)\s*:\s*$|^\s*function\s+([A-Za-z_]\w*)\s*\(", re.IGNORECASE)
COMMENT_RX    = re.compile(r"//.*?$|/\*.*?\*/", re.DOTALL | re.MULTILINE)
LOOP_RX       = re.compile(r"\b(for|while)\b", re.IGNORECASE)

def strip_comments(code:str) -> str:
    return re.sub(COMMENT_RX, "", code)

def parse_symbols(path: pathlib.Path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    code = strip_comments(raw)
    vars_assigned = [m.group(1) for m in VAR_ASSIGN_RX.finditer(code)]
    funcs = []
    for m in FUNC_DEF_RX.finditer(code):
        name = m.group(1) or m.group(3)
        if name: funcs.append(name)
    loop_warnings = []
    for block in re.split(r"[{}]", code):
        if LOOP_RX.search(block):
            for m in VAR_ASSIGN_RX.finditer(block):
                loop_warnings.append(m.group(1))
    return set(vars_assigned), set(funcs), set(loop_warnings)

def main():
    files = list(SRC_DIR.rglob("*.afl"))
    if not files:
        print("No .afl files found under src/", file=sys.stderr)
        sys.exit(0)

    var_map = collections.defaultdict(list)
    func_map = collections.defaultdict(list)
    loop_map = collections.defaultdict(list)

    for f in files:
        v, fn, lw = parse_symbols(f)
        for x in v:  var_map[x].append(f)
        for x in fn: func_map[x].append(f)
        for x in lw: loop_map[x].append(f)

    exit_code = 0
    clashes_vars  = {k:v for k,v in var_map.items()  if len(v) > 1}
    clashes_funcs = {k:v for k,v in func_map.items() if len(v) > 1}

    if clashes_vars:
        print("\n[CLASH] Trùng tên BIẾN giữa nhiều file:")
        for name, paths in sorted(clashes_vars.items()):
            print(f"  - {name}: " + ", ".join(str(p.relative_to(SRC_DIR.parent)) for p in paths))
        exit_code = 1

    if clashes_funcs:
        print("\n[CLASH] Trùng tên HÀM giữa nhiều file:")
        for name, paths in sorted(clashes_funcs.items()):
            print(f"  - {name}: " + ", ".join(str(p.relative_to(SRC_DIR.parent)) for p in paths))
        exit_code = 1

    if loop_map:
        print("\n[WARN] Gán biến trong khối loop (kiểm tra side effects/efficiency):")
        for name, paths in sorted(loop_map.items()):
            print(f"  - {name}: " + ", ".join(str(p.relative_to(SRC_DIR.parent)) for p in paths))

    if exit_code == 0:
        print("OK: Không phát hiện trùng tên biến/hàm.")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()