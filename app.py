from flask import Flask, render_template
import boto3

app = Flask(__name__)

# --- S3 Monitoring ---
def get_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        buckets.append({
            'name': bucket['Name'],
            'creation_date': bucket['CreationDate']
        })
    return buckets

# --- EC2 Monitoring ---
def get_ec2_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'id': instance.get('InstanceId'),
                'type': instance.get('InstanceType'),
                'state': instance['State']['Name'],
                'az': instance['Placement']['AvailabilityZone']
            })
    return instances

# --- IAM User Monitoring ---
def get_iam_users():
    iam = boto3.client('iam')
    response = iam.list_users()
    users = []
    for user in response['Users']:
        users.append({
            'username': user['UserName'],
            'created_at': user['CreateDate']
        })
    return users

# --- Route ---
@app.route('/')
def dashboard():
    ec2_instances = get_ec2_instances()
    s3_buckets = get_s3_buckets()
    iam_users = get_iam_users()
    return render_template('dashboard.html',
                           ec2_instances=ec2_instances,
                           s3_buckets=s3_buckets,
                           iam_users=iam_users)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
