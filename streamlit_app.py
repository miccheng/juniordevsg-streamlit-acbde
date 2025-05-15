import streamlit as st

st.title("My first Streamlit app")
st.write(
    "Hello streamlit world!"
)
name = st.text_input("Enter your name")

if name:
    st.write(f"Hello, {name}")

button = st.button("Click me")

if button:
    st.write("I was clicked!")
else:
    st.write("Waiting to be clicked")

st.checkbox("Check me")