import json
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_mail(config_object_json, report_object_path, charset='utf-8'):
    aws_ses = boto3.client('ses')
    try:
        mail_from = config_object_json['from']
        mail_to = config_object_json['to']
        mail_filename = config_object_json['filename']
        mail_subject = config_object_json['subject']
        mail_body_html = config_object_json['body_html']
        mail_body_plain = config_object_json['body_plain']
    except KeyError:
        raise Exception("Config File Exception: It doesnt have the required structure")
    
    ###
    # Sending email with AmazonSES
    msg = MIMEMultipart('mixed')
    msg['Subject'] = mail_subject 
    msg['From'] = mail_from 
    msg['To'] = ', '.join(mail_to)

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(mail_body_plain, 'plain', charset)
    htmlpart = MIMEText(mail_body_html, 'html', charset)
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    with open(report_object_path,'rb') as file:
        att = MIMEApplication(file.read(), Name='report.zip')

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header('Content-Disposition','attachment',filename=mail_filename)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    msg.attach(att)

    try:
        response_email = aws_ses.send_raw_email(
            Source=mail_from,
            Destinations=mail_to,
            RawMessage={
                'Data':msg.as_string(),
            }
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        raise ValueError("Sending-Email: "+getattr(e, 'message', repr(e)))
    else:
        print("Email sent! Message ID:" + response_email['MessageId'])
        return 0