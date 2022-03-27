from flask import Flask, jsonify, make_response, request, render_template
from dotenv import load_dotenv, find_dotenv
import os
import boto3

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


@app.route("/signup", methods=['POST'])
def signup_form():
    # gets username and password from the form
    username = request.form['username']
    password = request.form['password']

    client = boto3.client("cognito-idp", region_name="us-east-1")

    # sign-up on Cognito
    response = client.sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username=username,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": username}],
    )
    return jsonify(message='Signed')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
