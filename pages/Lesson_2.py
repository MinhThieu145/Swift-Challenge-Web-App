import streamlit as st
import boto3

# the title
st.title('Hey, now is the ELB, let goooo!!!.')

# get the name of the Ec2 that the script is currently running on
ec2 = boto3.client('ec2')
response = ec2.describe_instances()
instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

# print the instance id
st.write(f"Instance ID: {instance_id}")

# instance name
instance_name = response['Reservations'][0]['Instances'][0]['Tags'][0]['Value']
st.write(f"Instance Name: {instance_name}")