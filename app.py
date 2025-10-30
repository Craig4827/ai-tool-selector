
import streamlit as st
import json

st.set_page_config(page_title="AI Tool Selector Pro", page_icon="🤖", layout="centered")

with open("data/tools_snapshot.json", "r") as f:
    data = json.load(f)

st.title("🤖 AI Tool Selector — Snapshot (JSON)")

# search bar for tools
query = st.text_input("Search tools or activities (optional)")

bfuncs = sorted(list(data.get("business_functions", {}).keys()))
bfunc = st.selectbox("Business Function", [""] + bfuncs)

if bfunc:
    tool_types = sorted(list(data["business_functions"][bfunc].keys()))
    tt = st.selectbox("AI Tool Type", [""] + tool_types)
    if tt:
        st.subheader(f"Tools for {tt}")
        tools = data["business_functions"][bfunc][tt].get("tools", [])
        
        # optional filtering by rating level
        rating_filter = st.multiselect("Filter by rating values (text)", options=["High", "Medium", "Low"], default=[])
        # sort options
        sort_by = st.selectbox("Sort tools by", ["Default", "Name", "Cost"])
        
        def rating_match(tool):
            if not rating_filter:
                return True
            # Check any rating field contains one of the selected filters
            vals = [v for v in tool.get("ratings", {}).values()]
            for rf in rating_filter:
                if any(str(v).strip().lower() == rf.lower() for v in vals):
                    return True
            return False
        
        # apply query filter
        out_tools = []
        for t in tools:
            if query:
                q = query.lower()
                if q in t["name"].lower() or any(q in a.lower() for a in t.get("activities", [])) :
                    pass
                else:
                    continue
            if rating_match(t):
                out_tools.append(t)
        
        # sorting
        if sort_by == "Name":
            out_tools = sorted(out_tools, key=lambda x: x["name"].lower())
        elif sort_by == "Cost":
            out_tools = sorted(out_tools, key=lambda x: x.get("cost") or "")
        
        if not out_tools:
            st.info("No tools match the selected filters.")
        else:
            for t in out_tools:
                with st.expander(t["name"]):
                    cols = st.columns([2,1])
                    with cols[0]:
                        st.write("**Ratings:**")
                        rr = t.get("ratings", {})
                        if rr:
                            for k,v in rr.items():
                                st.markdown(f"- **{k}** : {v}")
                        else:
                            st.write("No rating available.")
                        st.write("**Activities:**")
                        # activities are only present at the business function -> type level; try to display from that level
                        b_acts = data["business_functions"][bfunc][tt].get("activities", [])
                        if b_acts:
                            for a in b_acts:
                                st.write(f"- {a}")
                    with cols[1]:
                        st.write("**Cost**")
                        st.write(t.get("cost") or "Unknown")
                        st.markdown("""<br>""", unsafe_allow_html=True)
                        st.button(f"Select {t['name']}", key=f"select_{t['name']}")
