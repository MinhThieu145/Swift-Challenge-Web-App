import streamlit as st
import boto3

# the title
st.title('Hey, now is the ELB, let goooo!!!.')

import boto3

# Create an EC2 resource instance
ec2 = boto3.resource('ec2')

# Get the current instance ID
instance_id = boto3.client('ec2').describe_instances(Filters=[
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
])['Reservations'][0]['Instances'][0]['InstanceId']

# Use the instance ID to get detailed information
instance = ec2.Instance(instance_id)

# st.write some details about the instance
st.write(f"Instance ID: {instance.id}")
st.write(f"Instance Type: {instance.instance_type}")
st.write(f"Public IPv4 Address: {instance.public_ip_address}")
st.write(f"AMI ID: {instance.image_id}")
st.write(f"State: {instance.state['Name']}")
