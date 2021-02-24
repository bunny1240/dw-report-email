import json
import urllib.parse
import boto3
from .delete_s3_object import delete_s3_object

def delete_files_in_s3_folder(bucket_name, folder_path):
    s3_client = boto3.client('s3')
    
    try:
        list_of_objects = s3_client.list_objects_v2(
            Bucket=bucket_name,
            MaxKeys=50,
            Prefix=folder_path
        )
        for content in list_of_objects.get('Contents'):
            if(content.get('Key') != folder_path):
                print("Deleting "+content.get('Key')+"..." )
                delete_s3_object(bucket_name, content.get('Key'))
    
    except Exception as e:
        raise ValueError("Deleting Files in Folder:"+folder_path+" :: "+getattr(e, 'message', repr(e)))