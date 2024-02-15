import streamlit as st
import boto3

# the title
st.title('Hey, now is the ELB, let goooo!!!.')


import subprocess

cmd='''set -o pipefail && sudo grep instance-id /run/cloud-init/instance-data.json | head -1 | sed 's/.*\"i-/i-/g' | sed 's/\",//g\''''    
status, instance_id = subprocess.getstatusoutput(cmd)
st.write(status, instance_id)

