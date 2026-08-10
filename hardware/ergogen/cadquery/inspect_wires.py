#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["cadquery>=2.4"]
# ///
import sys
from pathlib import Path
import cadquery as cq
from cadquery import importers

p = Path(sys.argv[1])
wp = importers.importDXF(str(p))
w = wp.wires().vals()[0]
print("wire type:", type(w))
print("dir:", [a for a in dir(w) if not a.startswith("__")])
try:
    print("has isClosed?", hasattr(w, "isClosed"), w.isClosed if hasattr(w, "isClosed") else None)
except Exception as e:
    print("isClosed error:", e)
try:
    print("Closed attr?", hasattr(w, "Closed"), getattr(w, "Closed", None))
except Exception as e:
    print("Closed attr error:", e)
try:
    print("Area?", hasattr(w, "Area"))
except Exception as e:
    print("Area attr error:", e)
