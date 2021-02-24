import json
import urllib.parse
import boto3

def get_s3_object(bucket_name, key, charset='utf-8'):
    aws_s3 = boto3.client('s3')
    key = urllib.parse.unquote_plus(key)
    try:
        return aws_s3.get_object(Bucket=bucket_name, Key=key)
    except Exception as e:
        raise ValueError("Get-S3-Key:"+key+" :: "+getattr(e, 'message', repr(e)))