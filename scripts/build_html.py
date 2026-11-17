"""Render a Markdown report and optional JSON registries as standalone HTML."""
import argparse
import html
import json
import subprocess
import tempfile
from pathlib import Path

CSS = """
:root { color-scheme: light; --ink: #1b2430; --muted: #5d6875; --line: #d8dee6; --paper: #fff; --accent: #1d4ed8; }
* { box-sizing: border-box; }
body { margin: 0; background: #f3f5f7; color: var(--ink); font: 16px/1.75 system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
main { max-width: 980px; margin: 0 auto; background: var(--paper); min-height: 100vh; padding: 48px clamp(20px, 5vw, 76px); }
body { max-width: 980px; margin: auto; padding: 2rem; background: white; overflow-wrap: anywhere; }
img { max-width: 100%; height: auto; }
table { display: block; overflow-x: auto; }
h1, h2, h3 { line-height: 1.25; margin-top: 1.7em; }
h1 { border-bottom: 2px solid var(--ink); padding-bottom: .35em; }
h2 { border-bottom: 1px solid var(--line); padding-bottom: .25em; }
a { color: var(--accent); }
table { border-collapse: collapse; width: 100%; margin: 1em 0 1.5em; font-size: .94em; }
th, td { border: 1px solid var(--line); padding: .55em .7em; text-align: left; vertical-align: top; }
th { background: #eef2f7; }
blockquote { margin-left: 0; border-left: 4px solid var(--accent); padding: .2em 1em; color: var(--muted); }
code, pre { background: #f1f3f5; border-radius: 4px; }
code { padding: .1em .3em; }
pre { padding: 1em; overflow: auto; }
.meta { color: var(--muted); font-size: .9em; }
@media print { body { background: white; } main { max-width: none; padding: 0; } a { color: inherit; text-decoration: none; } }
"""




def registry_html(title, data):
    def render(value):
        if isinstance(value, dict):
            return '<dl>' + ''.join('<dt><strong>' + html.escape(str(k)) + '</strong></dt><dd>' + render(v) + '</dd>' for k, v in value.items()) + '</dl>'
        if isinstance(value, list):
            return '<ol>' + ''.join('<li>' + render(v) + '</li>' for v in value) + '</ol>'
        return html.escape(str(value))
    return f"<!doctype html><html lang='th'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{html.escape(title)}</title><style>{CSS}</style></head><body><main><h1>{html.escape(title)}</h1>{render(data)}</main></body></html>"


def main_from_values(source_path, output_path, title):
    source = Path(source_path).resolve()
    output = Path(output_path).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        stylesheet = Path(temporary) / 'report.css'
        stylesheet.write_text(CSS, encoding='utf-8')
        subprocess.run([
            'pandoc', str(source), '--from=markdown-raw_html', '--to=html5',
            '--standalone', '--embed-resources', '--toc',
            '--metadata', 'lang=th', '--metadata', 'title=' + title,
            '--css', str(stylesheet), '--output', str(output),
        ], cwd=source.parent, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", default="รายงาน")
    args = parser.parse_args()
    main_from_values(args.source, args.output, args.title)
    print(json.dumps({"ok": True, "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
