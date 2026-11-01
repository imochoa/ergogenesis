#!/usr/bin/env python3
"""Mirror an ASCII STL across the X axis (negate X coordinates).

A reflection flips handedness, so each facet's vertex order is reversed and
the X component of its normal negated; otherwise the mirrored mesh would be
inside-out (inward-facing normals, negative volume).

Usage: mirror_stl_x.py <input.stl> <output.stl>
"""
import sys


def _negate_x(line: str, index: int) -> str:
    parts = line.split()
    parts[index] = str(-float(parts[index]))
    return " ".join(parts) + "\n"


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.stl> <output.stl>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    with open(sys.argv[2], "w") as f:
        vertices = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("facet normal "):
                f.write(_negate_x(line, 2))
            elif stripped.startswith("vertex "):
                vertices.append(_negate_x(line, 1))
            else:
                if stripped.startswith("endloop"):
                    f.writelines(reversed(vertices))
                    vertices = []
                f.write(line)

    print(f"mirrored {sys.argv[1]} -> {sys.argv[2]}")

if __name__ == "__main__":
    main()
