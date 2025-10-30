import streamlit as st
import json

st.set_page_config(page_title="AI Tool Selector", page_icon="🤖", layout="centered")

with open("data/tools.json") as f:
    data = json.load(f)

st.title("🤖 AI Tool Selector")
st.write("Choose a **Business Function**, then select an **AI Tool Type** to see recommended tools.")

function = st.selectbox("Business Function", [""] + list(data.keys()))

if function:
    tool_types = list(data[function]["AI Tool Types"].keys())
    tool_type = st.selectbox("AI Tool Type", [""] + tool_types)

    if tool_type:
        st.subheader("Recommended Tools")
        for tool in data[function]["AI Tool Types"][tool_type]:
            st.markdown(f"- [{tool['name']}]({tool['url']})")

st.markdown("---")
st.caption("Built with Streamlit · 2025")
