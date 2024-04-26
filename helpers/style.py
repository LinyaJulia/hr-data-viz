import streamlit as st

# Local CSS
# Usage: 
# Create a style.css file under helpers (or wherever) and add your styles
# Run local_css("helpers/style.css") in your main file to apply styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)