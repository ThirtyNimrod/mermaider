# mermaider

A local Streamlit app for writing and previewing [Mermaid](https://mermaid.js.org/) diagrams.

- Left panel: a text area for Mermaid code, with **Clear** and **Preview** buttons.
- Right panel: an interactive (pan/zoom) live preview, with buttons to download the
  diagram as a transparent-background **PNG** and the source as a **.txt** file.

## Setup

Requires **Python 3.9–3.13** (Python 3.14 is not yet supported by Streamlit) and Node.js (used only to run `mermaid-cli` for PNG export).

```bash
pip install -r requirements.txt   # use Python 3.13 if you have 3.14 installed
npm install
```

`npm install` fetches `@mermaid-js/mermaid-cli`, which bundles its own headless Chromium —
this is a one-time download and needs an internet connection.

## Run

```bash
streamlit run app.py
# or, if Python 3.14 is your default:
python3.13 -m streamlit run app.py
```

## How it works

- The live preview renders entirely in the browser using a vendored copy of `mermaid.js`
  and `svg-pan-zoom.js` (see `assets/`), so it works offline once the app is running.
- PNG export shells out to the locally installed `mmdc` (`npx mmdc -b transparent`) via
  `mermaid_export.py`, so the exported diagram always has a transparent background.
