import boto3


class User():
    username = ""
    password = ""

    def __init__(self, username, password):
        self.username = username
        self.password = password


def signin(user: User, os):
    client = boto3.client("cognito-idp", region_name="us-east-1")

    # Initiating the Authentication
    # USER_PASSWORD_AUTH needs to be configured on Cognito (General Settings > App Client > Auth Flow Configuration)
    response = client.initiate_auth(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": user.username, "PASSWORD": user.password},
    )

    # Getting the user AccessToken details from the JSON response
    access_token = response["AuthenticationResult"]["AccessToken"]

    response = client.get_user(AccessToken=access_token)

    return response
