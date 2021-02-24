import json
import urllib.parse
from .get_s3_object import get_s3_object

def get_config_object(bucket_name, s3_key):
    s3_key = urllib.parse.unquote_plus(s3_key)
    folder_name = get_folder_name(s3_key)
    config_key = 'config/'+folder_name+'/config.json'
    return get_s3_object(bucket_name, config_key)

def get_folder_name(s3_key):
    s3_key = urllib.parse.unquote_plus(s3_key)
    key_splitted = s3_key.split("/")
    if(len(key_splitted) == 3): #If the object key has the right structure composed by 3 parts: e.g. data/PKG_ISMI_DELTAS/report.csv
        if(len(key_splitted[2]) > 0 ):
            try:
                key_splitted.pop(0) # Removing e.g. data
                key_splitted.pop(1) # Removing e.g. report.csv
            except IndexError:
                raise Exception('Config File Exception: The file pushed on S3 is not located into one report folder.')
            return "".join(key_splitted) # Returning e.g. PKG_ISMI_DELTAS
        else:
            raise Exception('ERROR: Nothing to send, you only created a folder.')
    else:
        raise Exception('Config File Exception: The file pushed on S3 is not located into one report folder.')