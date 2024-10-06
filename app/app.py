import streamlit as st
import requests

st.title("Random Joke Generator")

if st.button("Get a Random Joke"):
    st.spinner()
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    # response = requests.post("https://api.example.com/endpoint", json={"key": "value"})
    
    if response.status_code == 200:
        joke = response.json()
        
        st.subheader(joke['setup'])
        st.write(joke['punchline'])
    else:
        st.error("Failed to fetch joke. Try again!")
