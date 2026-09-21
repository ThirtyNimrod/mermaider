"""PNG export for Mermaid diagrams via the local mermaid-cli (mmdc) install."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

_PUPPETEER_CONFIG = str(Path(__file__).parent / "puppeteer-config.json")


class MermaidExportError(RuntimeError):
    """Raised when a Mermaid diagram cannot be exported to PNG."""


def _find_npx() -> str:
    npx = shutil.which("npx")
    if npx is None:
        raise MermaidExportError(
            "Could not find `npx`. Install Node.js, then run `npm install` "
            "in the project root to set up mermaid-cli."
        )
    return npx


def export_png(code: str) -> bytes:
    """Render Mermaid `code` to a transparent-background PNG and return its bytes."""
    npx = _find_npx()
    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = os.path.join(tmp_dir, "diagram.mmd")
        output_path = os.path.join(tmp_dir, "diagram.png")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(code)

        result = subprocess.run(
            [
                npx, "mmdc",
                "-i", input_path,
                "-o", output_path,
                "-b", "transparent",
                "-p", _PUPPETEER_CONFIG,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise MermaidExportError(
                result.stderr.strip() or "mermaid-cli failed to render the diagram."
            )

        if not os.path.exists(output_path):
            raise MermaidExportError("mermaid-cli exited successfully but produced no output file.")

        with open(output_path, "rb") as f:
            return f.read()
