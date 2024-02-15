import streamlit as st
import boto3
import requests

# the title
st.title('Hey, now is the ELB, let goooo!!!.')

st.write('Below, you will find the IP of the machine that you are on (or the IP V4 of the EC2).')

base="https://checkip.amazonaws.com/"
req = requests.get(base)

# print the IP
st.info(f"Your IP is: {req.text}", icon="📝")
