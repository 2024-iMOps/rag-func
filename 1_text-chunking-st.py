import streamlit as st
from TextChunking import (
    split_by_character, 
    recursively_split_by_character,
)

with open(
    f"/workspace/card/2_iM Z체크카드(한국부동산원)/parse_results.md", "r", encoding="utf-8") as file:
    md_data = file.read()


st.title("Text Chunking")

chunking_method = st.selectbox(
    "Choose chunking method",
    [
        "Split by Character",
        "Recursively Split by Character",
        # "Semantic",
    ],
)

if chunking_method == "Split by Character":
    chunk_size = st.slider(
        "Chunk Size",
        min_value=128,
        max_value=1024,
        value=256,
        step=1,
    )

    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=16,
        max_value=256,
        value=32,
        step=1,
    )

    if st.button("Save Chunking"):
        chunks = split_by_character(md_data, int(chunk_size), int(chunk_overlap))
        st.write(f"split len: {len(chunks)}, ({chunk_size}, {chunk_overlap})")

elif chunking_method == "Recursively Split by Character":
    chunk_size = st.slider(
        "Chunk Size",
        min_value=128,
        max_value=1024,
        value=256,
        step=1,
    )

    chunk_overlap = st.slider(
        "Chunk Overlap",
        min_value=16,
        max_value=256,
        value=32,
        step=1,
    )

    if st.button("Save Chunking"):
        chunks = recursively_split_by_character(md_data, int(chunk_size), int(chunk_overlap))
        st.write(f"split len: {len(chunks)}, ({chunk_size}, {chunk_overlap})")

# elif chunking_method == "Semantic":
#     pass