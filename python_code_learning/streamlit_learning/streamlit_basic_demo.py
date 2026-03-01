import streamlit as st
st.title("My First Streamlit application")
name=st.text_input("Enter your name")

if st.button("Welcome"):
    if name:
        st.success(f"Welcome to Streamlit, {name}!")
    else:
        st.warning("Please enter your name to get a welcome message.")