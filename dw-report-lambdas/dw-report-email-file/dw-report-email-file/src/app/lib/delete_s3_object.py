import json
import urllib.parse
import boto3

def delete_s3_object(bucket_name, key, charset='utf-8'):
    aws_s3 = boto3.client('s3')
    key = urllib.parse.unquote_plus(key)
    try:
        return aws_s3.delete_object(Bucket=bucket_name, Key=key)
    except Exception as e:
        raise ValueError("Delete-S3-Key:"+key+" :: "+getattr(e, 'message', repr(e)))