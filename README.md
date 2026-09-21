# mermaider

A local Streamlit app for writing and previewing [Mermaid](https://mermaid.js.org/) diagrams.

- Left panel: a text area for Mermaid code, with **Clear** and **Preview** buttons.
- Right panel: an interactive (pan/zoom) live preview, with buttons to download the
  diagram as a transparent-background **PNG** and the source as a **.txt** file.

## Prerequisites & Setup

### 1. Python Environment
Requires **Python 3.9–3.13** (Python 3.14 is not yet supported by Streamlit).

```bash
pip install -r requirements.txt   # use Python 3.13 if you have 3.14 installed
```

### 2. Node.js & NPM Dependencies
Requires **Node.js 18+** with `npm` and `npx` available on your system `PATH`.

The primary NPM element required by this project is:
- **`@mermaid-js/mermaid-cli`**: Supplies the `mmdc` command-line tool used by `mermaid_export.py` to render high-resolution, transparent PNGs via headless Chromium.

To install dependencies specified in `package.json`:
```bash
npm install
```

Alternatively, you can install the Mermaid CLI directly:
```bash
npm install --save-dev @mermaid-js/mermaid-cli
```

> **Note**: During `npm install`, Puppeteer downloads a bundled headless Chromium instance for diagram rendering. This requires an active internet connection on initial installation. Headless browser flags are managed in `puppeteer-config.json`.
>
> *(Note: The in-app interactive preview uses the pre-bundled scripts in `assets/`, so no web bundler or build step is needed.)*

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
