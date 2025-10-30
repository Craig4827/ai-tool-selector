# AI Tool Selector Pro — Updated (3-step flow)

This Streamlit app enforces the exact 3-step interaction:
1. Select Business Function
2. Select AI Tool Type (applicable to the chosen Business Function)
3. View recommended tools with ratings and cost

Data is read from `data/tools_snapshot.json` (snapshot generated from your Excel).

Run locally:
```
pip install -r requirements.txt
streamlit run app.py
```
