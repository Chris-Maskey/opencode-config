#!/usr/bin/env python3
"""
Render an .excalidraw file to PNG using Playwright.
Usage: uv run python render_excalidraw.py <path-to-file.excalidraw>
Output: PNG saved next to the .excalidraw file (same name, .png extension)
"""

import sys
import json
import base64
import os
from pathlib import Path


def render_excalidraw(excalidraw_path: str) -> str:
    from playwright.sync_api import sync_playwright

    path = Path(excalidraw_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path) as f:
        data = json.load(f)

    out_path = path.with_suffix(".png")

    # HTML that loads excalidraw from CDN, imports the scene, and exports
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: white; }}
  #root {{ width: 100vw; height: 100vh; }}
</style>
</head>
<body>
<div id="root"></div>
<script type="module">
  import {{ createRoot }} from 'https://esm.sh/react-dom@18/client';
  import React from 'https://esm.sh/react@18';
  import Excalidraw, {{ exportToBlob }} from 'https://esm.sh/@excalidraw/excalidraw@0.17.6';

  const scene = {json.dumps(data)};
  let excalidrawAPI = null;

  function App() {{
    return React.createElement(
      Excalidraw.Excalidraw || Excalidraw.default || Excalidraw,
      {{
        initialData: scene,
        excalidrawAPI: (api) => {{ excalidrawAPI = api; }},
        viewModeEnabled: true,
      }}
    );
  }}

  const root = createRoot(document.getElementById('root'));
  root.render(React.createElement(App));

  // Wait for render then export
  async function doExport() {{
    await new Promise(r => setTimeout(r, 3000));
    if (!excalidrawAPI) {{
      window.__exportError = 'no api';
      return;
    }}
    try {{
      const elements = excalidrawAPI.getSceneElements();
      const appState = excalidrawAPI.getAppState();
      const blob = await exportToBlob({{
        elements,
        appState: {{ ...appState, exportBackground: true, exportWithDarkMode: false }},
        files: null,
        getDimensions: () => ({{ width: 3000, height: 2400, scale: 1 }}),
      }});
      const reader = new FileReader();
      reader.onloadend = () => {{
        window.__exportData = reader.result;
      }};
      reader.readAsDataURL(blob);
    }} catch(e) {{
      window.__exportError = String(e);
    }}
  }}
  doExport();
</script>
</body>
</html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 3000, "height": 2400})

        page.set_content(html)

        # Wait for export
        try:
            page.wait_for_function(
                "window.__exportData !== undefined || window.__exportError !== undefined",
                timeout=30000,
            )
        except Exception as e:
            # Fallback: screenshot the whole page
            print(
                f"  [warn] JS export timed out ({e}), falling back to full-page screenshot"
            )
            page.screenshot(path=str(out_path), full_page=True)
            browser.close()
            print(f"Saved: {out_path}")
            return str(out_path)

        error = page.evaluate("window.__exportError")
        if error:
            print(f"  [warn] Export error: {error}, falling back to screenshot")
            page.screenshot(path=str(out_path), full_page=True)
            browser.close()
            print(f"Saved: {out_path}")
            return str(out_path)

        data_url = page.evaluate("window.__exportData")
        browser.close()

        # Decode base64 data URL
        header, encoded = data_url.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        with open(out_path, "wb") as f:
            f.write(img_bytes)

    print(f"Saved: {out_path}")
    return str(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python render_excalidraw.py <path-to-file.excalidraw>")
        sys.exit(1)
    render_excalidraw(sys.argv[1])
