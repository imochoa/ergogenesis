#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "cadquery>=2.4",
# ]
# ///
import sys
from pathlib import Path
import cadquery as cq
from cadquery import importers

p = Path(sys.argv[1])
obj = importers.importDXF(str(p))
print("type:", type(obj))
print("repr:", obj)
print("dir:", [a for a in dir(obj) if not a.startswith("__")])
try:
    print("is Compound?", isinstance(obj, cq.Compound))
except Exception as e:
    print("is Compound?", e)
try:
    print("has .Wires?", hasattr(obj, "Wires"))
except Exception as e:
    print("has Wires?", e)
try:
    print("has .wires()?", hasattr(obj, "wires") )
except Exception as e:
    print("has wires?", e)
try:
    if hasattr(obj, "wires"):
        print("wires() ->", type(obj.wires()))
        vals = obj.wires().vals()
        print("wires().vals len:", len(vals))
except Exception as e:
    print("wires() error:", e)
