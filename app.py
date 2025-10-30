import streamlit as st
import json
from html import escape

st.set_page_config(page_title="AI Tool Selector — Updated", page_icon="🤖", layout="centered")

# load snapshot JSON
with open("data/tools_snapshot.json", "r") as f:
    data = json.load(f)

st.title("🤖 AI Tool Selector — Updated (3-step flow)")
st.write("Follow the steps: 1) Select Business Function → 2) Select AI Tool Type → 3) View recommended tools with ratings and cost.")

# Step 1: select business function
bfuncs = sorted(data.get("business_functions", {}).keys())
bfunc = st.selectbox("1) Select Business Function", [""] + bfuncs, help="Choose the business function you want to support")

if not bfunc:
    st.info("Please select a Business Function to proceed to Step 2.")
    st.stop()

# Step 2: show applicable AI Tool Types for selected business function
tool_types = sorted(list(data["business_functions"].get(bfunc, {}).keys()))
tt = st.selectbox("2) Select AI Tool Type (applicable to the chosen Business Function)", [""] + tool_types, help="Tool types that are applicable for the selected business function")

if not tt:
    st.info("Please select an AI Tool Type to see recommended tools.")
    st.stop()

# Step 3: show recommended tools for selected tool type
st.subheader(f"3) Recommended AI Tools for **{tt}** (under **{bfunc}**)")
tools = data["business_functions"][bfunc][tt].get("tools", [])

if not tools:
    st.warning("No tools found for this selection.")
else:
    # Optional: allow user to filter by rating text (High/Medium/Low) or cost
    cols_filter = st.columns([1,1,2])
    with cols_filter[0]:
        rating_filter = st.multiselect("Filter by rating", options=["High","Medium","Low"], help="Filter tools by rating text values (if available)")
    with cols_filter[1]:
        cost_filter = st.multiselect("Filter by cost (text)", options=sorted(list({t.get('cost') or 'Unknown' for t in tools})))
    with cols_filter[2]:
        search_q = st.text_input("Search tool name (optional)")

    def rating_match(tool):
        if not rating_filter:
            return True
        vals = [str(v).strip().lower() for v in tool.get("ratings", {}).values() if v is not None]
        return any(r.lower() in vals for r in rating_filter)

    def cost_match(tool):
        if not cost_filter:
            return True
        return (tool.get("cost") or "Unknown") in cost_filter

    # Apply filters
    filtered = []
    for t in tools:
        if search_q and search_q.lower() not in t.get("name","").lower():
            continue
        if not rating_match(t):
            continue
        if not cost_match(t):
            continue
        filtered.append(t)

    if not filtered:
        st.info("No tools match your filters.")
    else:
        # Display each tool with ratings and cost
        for t in filtered:
            name = t.get("name")
            ratings = t.get("ratings", {})
            cost = t.get("cost") or "Unknown"
            # Render a nice card-like block using markdown and columns
            st.markdown(f"""
            <div style="border:1px solid #e6e9ef; padding:12px; border-radius:8px; margin-bottom:10px; background: #ffffff;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:18px; font-weight:700;">{escape(name)}</div>
                <div style="font-size:14px; color:#555;">Cost: <strong>{escape(cost)}</strong></div>
              </div>
              <div style="margin-top:8px;">
            """, unsafe_allow_html=True)
            # Ratings table
            if ratings:
                for k,v in ratings.items():
                    # Color-code High/Medium/Low
                    val = str(v).strip()
                    color = "#2d9f5b" if val.lower()=="high" else ("#f2994a" if val.lower()=="medium" else ("#eb5757" if val.lower()=="low" else "#777"))
                    st.markdown(f"<span style='display:inline-block; padding:4px 8px; border-radius:6px; background:#f4f6fb; margin-right:6px;'><strong>{escape(k)}</strong>: <span style='color:{color};'>{escape(val)}</span></span>", unsafe_allow_html=True)
            else:
                st.write("No ratings available.")
            st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('---')
st.caption('Snapshot-based app. To update data, regenerate the JSON snapshot from the Excel.')
