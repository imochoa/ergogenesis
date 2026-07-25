#!/usr/bin/env python3
"""Mirror an ASCII STL across the X axis (negate X coordinates).

Usage: mirror_stl_x.py <input.stl> <output.stl>
"""
import sys

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.stl> <output.stl>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    with open(sys.argv[2], "w") as f:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("vertex "):
                parts = line.split()
                parts[1] = str(-float(parts[1]))
                f.write(" ".join(parts) + "\n")
            else:
                f.write(line)

    print(f"mirrored {sys.argv[1]} -> {sys.argv[2]}")

if __name__ == "__main__":
    main()
