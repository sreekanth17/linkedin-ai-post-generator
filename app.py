import streamlit as st
import pandas as pd
import os
import time
from openai import OpenAI

# --- UI ---
st.set_page_config(page_title="LinkedIn AI Post Generator", layout="centered")
st.title("🚀 LinkedIn AI Post Generator")
st.write("Upload Excel → Generate LinkedIn posts using GenAI")

# --- API Key ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY not set")
    st.stop()

client = OpenAI(api_key=api_key)

# --- Upload ---
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

def generate_post(row):
    prompt = f"""
You are a LinkedIn personal branding expert.

Audience: {row.Audience}
Pain Point: {row.Pain_Point}
Topic: {row.Topic_Idea}
Goal: {row.Post_Goal}

Rules:
- Hook in first 2 lines
- Short paragraphs
- Bullets where needed
- CTA at end
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.dataframe(df.head())

    if st.button("Generate LinkedIn Posts"):
        with st.spinner("Generating posts..."):
            df["LinkedIn_Post"] = df.apply(generate_post, axis=1)
            time.sleep(1)

        st.success("Posts generated!")
        st.dataframe(df)

        st.download_button(
            "Download Excel",
            df.to_excel(index=False),
            file_name="linkedin_posts_output.xlsx"
        )
