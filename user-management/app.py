from flask import Flask, jsonify, make_response, request, render_template
from dotenv import load_dotenv, find_dotenv
import os
import boto3
import pprint
from botocore.client import ClientError

app = Flask(__name__)

load_dotenv(find_dotenv())
# read the .env-sample, to load the environment variable.
dotenv_path = os.path.join(os.path.dirname(__file__), ".env-var")
load_dotenv(dotenv_path)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.route("/signup")
def sign_up():
    username = request.args.get('username')
    password = request.args.get('passwrd')

    client = boto3.client("cognito-idp", region_name="us-east-1")

    try:
        # Add user to pool
        sign_up_response = client.sign_up(
            ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
            Username=username,
            Password=password,
            UserAttributes=[{'Name': 'email',
                             'Value': username}])
        pprint(sign_up_response)
        return jsonify(message="User successful created")
    except ClientError as err:
        # Probably user already exists
        print(err)
        return jsonify(message="error")


@app.route("/auth")
def init_auth():
    username = request.args.get('username')
    password = request.args.get('passwrd')

    client = boto3.client("cognito-idp", region_name="us-east-1")

    # This is less secure, but simpler
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password},
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"))
    print("----- Log in response -----")
    pprint(response)
    print("---------------------------")

    # If authentication was successful we got three tokens
    print(response['AuthenticationResult']['AccessToken'])
    # response['AuthenticationResult']['IdToken']
    # response['AuthenticationResult']['RefreshToken']


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
