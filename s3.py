import boto3
from botocore.exceptions import ClientError

import config


def upload_file(content, s3_path):
    s3 = boto3.resource(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    try:
        response = s3.Object(config.BUCKET, s3_path).put(Body=content)
    except ClientError as e:
        (e)
        return False
    return True

def exist_file(s3_path):
    s3 = boto3.resource(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    try:
        response = s3.Object(config.BUCKET, s3_path).load()
    except ClientError as e:
        (e)
        return False
    return True

def get_file(s3_path):
    s3 = boto3.resource(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    response = s3.Object(config.BUCKET, s3_path).get()
    content = response["Body"].read()
    return content

def delete_files(s3_path):
    s3 = boto3.resource(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    bucket = s3.Bucket(config.BUCKET)
    bucket.objects.filter(Prefix=s3_path).delete()


if __name__ == "__main__":
    pass
    
    