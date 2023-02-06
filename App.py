import streamlit as st

st.set_page_config(
    page_title="Search PubMed 🔎"
)

st.write("# Welcome to PubMed Search! 🔎")

st.sidebar.success("Select an option above.")

st.markdown(
    """
    This App is built with Streamlit, an open-source app framework
    for Machine Learning and Data Science projects.
    **👈 Select an option from the sidebar** to see some examples
    of what Streamlit can do!
    ### What can this app do?
    - Enter a Search URL from PubMed and this app will create a dataframe containing title, keywords, abstract, etc
    - The table can be downloaded as a csv
    - Abstracts of articles are separated by paragraph in another table 
    - A dictionary of most common keywords in Dementia literature is used to identify matched keywords in abstract
    ### What is the aim of this app?
    - The aim of this app is to reduce the time taken to complete screening of titles/abstracts for systematic reviews
    - Your feedback helps improve the app and automate the screening of titles/abstracts
"""
)
