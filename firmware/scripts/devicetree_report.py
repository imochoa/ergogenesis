#!/usr/bin/env python3
"""Generate a self-contained HTML report from a Zephyr edt.pickle file.

Run inside the firmware devcontainer after a build:

    python3 scripts/devicetree_report.py .build/nice_nano/ergogenesis_left \
      .build/nice_nano/ergogenesis_left/zephyr/devicetree-report.html
"""

from __future__ import annotations

import argparse
import html
import pickle
import sys
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def format_value(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bytes):
        return value.hex(" ")
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(format_value(item) for item in value) + "]"
    if hasattr(value, "path"):
        return str(value.path)
    if hasattr(value, "controller") and hasattr(value, "data"):
        return f"{value.controller.path} {format_value(value.data)}"
    return str(value)


def property_rows(node) -> str:
    rows = []
    for name, prop in sorted(node.props.items()):
        spec = prop.spec
        description = prop.description or ""
        flags = []
        if spec.required:
            flags.append("required")
        if spec.deprecated:
            flags.append("deprecated")
        if spec.default is not None:
            flags.append(f"default: {format_value(spec.default)}")
        if spec.enum is not None:
            flags.append(f"allowed: {format_value(spec.enum)}")
        rows.append(
            "<tr>"
            f"<td><code>{esc(name)}</code></td>"
            f"<td><code>{esc(format_value(prop.val))}</code></td>"
            f"<td>{esc(prop.type)}</td>"
            f"<td>{esc(description)}</td>"
            f"<td>{esc('; '.join(flags))}</td>"
            "</tr>"
        )
    return "".join(rows) or "<tr><td colspan=5>No binding-defined properties.</td></tr>"


def node_html(node, depth: int = 0) -> str:
    compats = ", ".join(node.compats) or "no compatible"
    labels = ", ".join(node.labels)
    binding = node.binding_path or "no binding"
    description = node.description or ""
    properties = property_rows(node)
    children = "".join(node_html(child, depth + 1) for child in node.children.values())
    opened = " open" if depth < 2 else ""
    labels_html = f" · labels: {esc(labels)}" if labels else ""
    return f"""
<details{opened} data-search="{esc(' '.join([node.path, compats, labels, description]))}">
  <summary><code>{esc(node.path)}</code> <span class="status">{esc(node.status)}</span> · {esc(compats)}{labels_html}</summary>
  <section>
    <p>{esc(description)}</p>
    <dl>
      <dt>Binding</dt><dd><code>{esc(binding)}</code></dd>
      <dt>Dependency ordinal</dt><dd>{esc(node.dep_ordinal)}</dd>
    </dl>
    <table>
      <thead><tr><th>Property</th><th>Resolved value</th><th>Type</th><th>Binding documentation</th><th>Constraints</th></tr></thead>
      <tbody>{properties}</tbody>
    </table>
    {children}
  </section>
</details>"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir", type=Path, help="Build directory for one target")
    parser.add_argument("output", type=Path, help="HTML report path")
    args = parser.parse_args()

    build_dir = args.build_dir.resolve()
    pickle_path = build_dir / "zephyr" / "edt.pickle"
    if not pickle_path.is_file():
        parser.error(f"generated EDT data not found: {pickle_path}")

    # edt.pickle references classes from Zephyr's vendored devicetree package.
    firmware = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(firmware / "zephyr" / "scripts" / "dts" / "python-devicetree" / "src"))
    with pickle_path.open("rb") as file:
        edt = pickle.load(file)

    root = next(node for node in edt.nodes if node.parent is None)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(build_dir.name)} — devicetree report</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui,sans-serif; }} body {{ margin:1.5rem; }}
input {{ font:inherit; margin:.5rem 0 1rem; padding:.5rem; width:min(42rem,100%); }}
details {{ border-left:2px solid #8886; margin:.4rem 0 .4rem .5rem; padding:.25rem .75rem; }}
summary {{ cursor:pointer; }} section {{ margin:.75rem 0; }} dl {{ display:grid; grid-template-columns:max-content 1fr; gap:.25rem .75rem; }} dt {{ font-weight:bold; }} dd {{ margin:0; }}
table {{ border-collapse:collapse; font-size:.85rem; max-width:100%; }} th,td {{ border:1px solid #8886; padding:.4rem; text-align:left; vertical-align:top; }} td {{ white-space:pre-wrap; }} code {{ font-family:ui-monospace,monospace; }} .status {{ color:#16803c; font-weight:bold; }}
</style></head><body>
<h1>{esc(build_dir.name)} — devicetree report</h1>
<p>Resolved nodes, binding documentation, and property values from Zephyr's generated <code>edt.pickle</code>.</p>
<label>Search <input id="search" type="search" autofocus placeholder="node path, compatible, label, or description"></label>
<div id="tree">{node_html(root)}</div>
<script>
const nodes=[...document.querySelectorAll('details')], input=document.querySelector('#search');
input.addEventListener('input',()=>{{const q=input.value.toLowerCase(); for(const node of nodes){{const match=node.textContent.toLowerCase().includes(q); node.hidden=!match; if(match&&q) node.open=true;}}}});
</script></body></html>"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(page, encoding="utf-8")
    print(f"Wrote {args.output} ({len(edt.nodes)} nodes)")


if __name__ == "__main__":
    main()
