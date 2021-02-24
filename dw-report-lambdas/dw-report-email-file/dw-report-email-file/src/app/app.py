import json
import newrelic.agent
from .lib.get_s3_object import get_s3_object
from .lib.get_config_object import get_config_object
from .lib.get_config_object import get_folder_name
from .lib.send_mail import send_mail
from .lib.delete_s3_object import delete_s3_object
from .lib.zip_files_in_s3_folder import zip_files_in_s3_folder
from .lib.delete_files_in_s3_folder import delete_files_in_s3_folder


def lambda_handler(event, context):
    charset = 'utf-8'
    ###
    # Retrieving the Report File
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
    except KeyError:
        raise Exception('ERROR: event parameter doesnt have the required structure, this function must be called from an S3 Notification.')
    
    report_folder_name = get_folder_name(key)
    ## Deleting the file which was sent on S3 to trigger this function
    delete_s3_object(bucket, key)
    # Adding custom parameter for new relic dashboards
    newrelic.agent.add_custom_parameter('report_name', report_folder_name)
    
    zip_file_name = zip_files_in_s3_folder(bucket, "data/"+report_folder_name+"/")
    ###
    # Retrieving Configuration File for The Report
    config_object = get_config_object(bucket, key)
    config_object_json = config_object["Body"].read().decode(charset)
    config_object_json = json.loads(config_object_json)

    ###
    # Sending Email
    send_mail(config_object_json, zip_file_name)
    delete_files_in_s3_folder(bucket, "data/"+report_folder_name+"/")
    return {
        "body": 'Finished',
        "statusCode": 200
    }