"""Local Mermaid diagram builder: write Mermaid code, preview it, export PNG/txt."""

import json
from pathlib import Path

import streamlit as st

from mermaid_export import MermaidExportError, export_png

ASSETS_DIR = Path(__file__).parent / "assets"
DEFAULT_CODE = "graph TD\n    A[Start] --> B{Decision}\n    B -->|Yes| C[Do thing]\n    B -->|No| D[Skip]\n"

st.set_page_config(page_title="Mermaider", layout="wide")


@st.cache_resource
def load_preview_libs() -> tuple[str, str]:
    mermaid_js = (ASSETS_DIR / "mermaid.min.js").read_text(encoding="utf-8")
    panzoom_js = (ASSETS_DIR / "svg-pan-zoom.min.js").read_text(encoding="utf-8")
    return mermaid_js, panzoom_js


def build_preview_html(code: str) -> str:
    mermaid_js, panzoom_js = load_preview_libs()
    code_json = json.dumps(code)
    return f"""
    <div id="diagram-wrap" style="width:100%;height:560px;overflow:hidden;
         border:1px solid #444;border-radius:6px;background:#0e1117;">
      <div id="diagram" style="width:100%;height:100%;"></div>
    </div>
    <script>{mermaid_js}</script>
    <script>{panzoom_js}</script>
    <script>
      const code = {code_json};
      const container = document.getElementById('diagram');
      if (!code.trim()) {{
        container.innerHTML = '<p style="color:#888;padding:1rem;">Nothing to preview yet.</p>';
      }} else {{
        mermaid.initialize({{ startOnLoad: false }});
        mermaid.render('generatedDiagram', code).then(({{ svg }}) => {{
          container.innerHTML = svg;
          const svgEl = container.querySelector('svg');
          svgEl.style.maxWidth = 'none';
          svgEl.style.width = '100%';
          svgEl.style.height = '100%';
          svgPanZoom(svgEl, {{
            zoomEnabled: true,
            controlIconsEnabled: true,
            fit: true,
            center: true,
          }});
        }}).catch((err) => {{
          container.innerHTML = '<pre style="color:#ff6b6b;white-space:pre-wrap;padding:1rem;">'
            + String(err) + '</pre>';
        }});
      }}
    </script>
    """


@st.cache_data(show_spinner="Rendering PNG...")
def cached_export_png(code: str) -> bytes:
    return export_png(code)


if "code" not in st.session_state:
    st.session_state.code = DEFAULT_CODE
if "previewed_code" not in st.session_state:
    st.session_state.previewed_code = st.session_state.code


def clear_code():
    st.session_state.code = ""
    st.session_state.previewed_code = ""


def preview_code():
    st.session_state.previewed_code = st.session_state.code


st.title("Mermaider")

left, right = st.columns(2)

with left:
    st.text_area("Mermaid code", key="code", height=520, label_visibility="collapsed")
    clear_col, preview_col = st.columns(2)
    clear_col.button("Clear", on_click=clear_code, use_container_width=True)
    preview_col.button("Preview", on_click=preview_code, type="primary", use_container_width=True)

with right:
    st.components.v1.html(build_preview_html(st.session_state.previewed_code), height=580, scrolling=False)

    png_bytes = None
    export_error = None
    if st.session_state.previewed_code.strip():
        try:
            png_bytes = cached_export_png(st.session_state.previewed_code)
        except MermaidExportError as exc:
            export_error = str(exc)

    if export_error:
        st.error(f"PNG export failed: {export_error}")

    png_col, txt_col = st.columns(2)
    with png_col:
        st.download_button(
            "Download PNG",
            data=png_bytes or b"",
            file_name="diagram.png",
            mime="image/png",
            disabled=png_bytes is None,
            use_container_width=True,
        )
    with txt_col:
        st.download_button(
            "Download Code (.txt)",
            data=st.session_state.code,
            file_name="diagram.txt",
            mime="text/plain",
            disabled=not st.session_state.code.strip(),
            use_container_width=True,
        )
