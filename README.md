# AI Tool Selector

A simple static web app that helps select AI Tool Types and recommended AI tools based on a chosen business function.

This package was generated from the user's AI Tool Matrix document.

## How it works

- Choose a **Business Function** from the first dropdown.
- The app shows **AI Tool Types** applicable to that function.
- Choose a Tool Type to see recommended tools (links included).

## Run locally

Open `index.html` in any modern web browser or serve the folder with a static server, e.g.:

```bash
# Python 3
python -m http.server 8000
# then open http://localhost:8000
```

## Files
- `index.html` - main UI
- `app.js` - client-side logic
- `styles.css` - styling
- `data/tools.json` - mapping of functions -> tool types -> tools
