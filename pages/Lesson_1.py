import streamlit as st
import boto3
import mimetypes

# Constants
AWS_ACCESS_KEY_ID = 'AKIATO37PU5KKLA2SIOA'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'swift-challenge-file-stores'
UID = 'swift-challenge-uid'

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)


# Initialize a session using Amazon S3 credentials
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# Create an S3 client
s3 = session.client('s3')

# Streamlit application starts here
st.title('Hey, welcome to your lesson 1')

st.write('In this lesson, we will work with S3, below you can try and upload a file on your own.')

st.subheader('Section 1: Uploading files to S3')

uploaded_files = st.file_uploader(label="Upload a file", accept_multiple_files=True, label_visibility='collapsed')

sucessful_uploads = []

# if uploaded_files is not an empty list
if uploaded_files:
    # iterate over the list of files
    for uploaded_file in uploaded_files:
        
        # got the file name, the file name would be the combination of UID and file name
        uploaded_file.name = f"{UID}/{uploaded_file.name}"

# add a tip here
st.info("Tip: To be able to view in browser, please upload files like PDF or PNG.", icon="📝")

if st.button('Upload to S3', key='primary'):
    for uploaded_file in uploaded_files:
        file_contents = uploaded_file.getvalue()
        object_name = f"{UID}/{uploaded_file.name}"

        # Infer the file type and set a default if unable to guess
        content_type = mimetypes.guess_type(uploaded_file.name)[0] or 'application/octet-stream'

        try:
            with st.spinner(f"Uploading '{uploaded_file.name}' to S3..."):
                response = s3.put_object(
                    Bucket=BUCKET_NAME, 
                    Key=object_name, 
                    Body=file_contents, 
                    ContentType=content_type  # Set the ContentType here
                )
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                st.toast(f"File '{uploaded_file.name}' uploaded successfully.", icon="🚀")
            else:
                st.toast(f"Failed to upload '{uploaded_file.name}'.", icon="⚠️")
        except Exception as e:
            st.toast(f"An error occurred while uploading '{uploaded_file.name}': {e}", icon="⚠️")
                
                
st.divider()

st.subheader('Section 2: List of successful uploads and getting the url of the file')
st.write('''You can view the files you have uploaded here. You can also open them in browswer and share the link with others. However, 
            the link will only last for 15 minutes.''')

# show all the files in the bucket, from the UID
response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=UID)

# if the response is not empty
if response['KeyCount'] > 0:
    # iterate over the list of files
    for file in response['Contents']:
        # get the url of the file
        url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': file['Key']}, ExpiresIn=3600)
        
        # only get the name of the file, not the UID
        file_name = file['Key'].split('/')[2]
        
        # for each of them has a container
        with st.container(border=True):
            st.write(f"File: {file_name}")
            
            # write open here, and add the url with markdown
            st.markdown(f"[Open]({url})")
                
# else, just say you have no files
else:
    st.error("It's a bit empty here, try uploading a file. 🤔")
            
            