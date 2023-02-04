import os


def handler(event, context):
    token = event["headers"].get("token")

    if token == os.environ["SERVERLESS_API_TOKEN"]:
        return generate_policy("user", "Allow", event["routeArn"])
    else:
        return generate_policy("user", "Deny", event["routeArn"])


def generate_policy(principal_id, effect, resource):
    auth_response = dict()

    auth_response["principalId"] = principal_id
    if effect and resource:
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource,
                },
            ],
        }
        auth_response["policyDocument"] = policy_document
    return auth_response
