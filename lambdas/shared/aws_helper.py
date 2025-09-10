# aws_helper.py
import os
import boto3
from decimal import Decimal


dynamo = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns = boto3.client('sns')


def get_table(table_name):
return dynamo.Table(table_name)


def put_item(table_name, item):
table = get_table(table_name)
table.put_item(Item=item)


def query_transactions_by_user(table_name, user_id, limit=100):
table = get_table(table_name)
resp = table.query(KeyConditionExpression='user_id = :u',
ExpressionAttributeValues={':u': user_id},
Limit=limit)
return resp.get('Items', [])


def save_html_to_s3(bucket, key, html_str):
s3.put_object(Bucket=bucket, Key=key, Body=html_str, ContentType='text/html')
return f"s3://{bucket}/{key}"


def publish_sns(topic_arn, subject, message):
sns.publish(TopicArn=topic_arn, Subject=subject, Message=message)
