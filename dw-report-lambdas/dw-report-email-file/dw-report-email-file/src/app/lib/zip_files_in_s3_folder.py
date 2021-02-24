import json
import urllib.parse
import boto3
from zipfile import ZipFile

def zip_files_in_s3_folder(bucket_name, folder_path):
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    zip_object = ZipFile('/tmp/report.zip', 'w')
    
    try:
        list_of_objects = s3_client.list_objects_v2(
            Bucket=bucket_name,
            MaxKeys=50,
            Prefix=folder_path
        )
        for content in list_of_objects.get('Contents'):
            if(content.get('Key') != folder_path):
                print("Downloading "+content.get('Key')+"..." )
                s3_resource.Bucket(bucket_name).download_file(content.get('Key'), '/tmp/'+get_file_name(content.get('Key')))
                zip_object.write('/tmp/'+get_file_name(content.get('Key')), get_file_name(content.get('Key')))
        return '/tmp/report.zip'
    except Exception as e:
        raise ValueError("Zipping Files of S3 Folder:"+folder_path+" :: "+getattr(e, 'message', repr(e)))

def get_file_name(s3_key):
    key_splitted = s3_key.split("/")
    if(len(key_splitted) == 3): #If the object key has the right structure composed by 3 parts: e.g. data/PKG_ISMI_DELTAS/report.csv
        if(len(key_splitted[2]) > 0 ):
            try:
                key_splitted.pop(0) # Removing e.g. data
                key_splitted.pop(0) # Removing e.g. PKG_ISMI_DELTAS
            except IndexError:
                raise Exception('Data File Exception: The file pushed on S3 is not located into one report folder.')
            return "".join(key_splitted) # Returning e.g. report.csv
        else:
            raise Exception('ERROR: Nothing to send, you only created a folder.')
    else:
        raise Exception('Data File Exception: The file pushed on S3 is not located into one report folder.')
