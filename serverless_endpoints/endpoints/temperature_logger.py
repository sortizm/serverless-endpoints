import os
from datetime import datetime

import boto3
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, CORSConfig
from aws_lambda_powertools.event_handler.api_gateway import Response

from serverless_endpoints import exception

temperature_table = boto3.resource(
    "dynamodb", region_name=os.getenv("AWS_REGION", "eu-west-1")
).Table("serverless_endpoints.temperature")

cors_config = CORSConfig()
app = APIGatewayHttpResolver(cors=cors_config)


@app.post("/temperature")
def log_temperature() -> Response:
    temperature = app.current_event.json_body["temperature"]
    humidity = app.current_event.json_body.get("humidity")
    where = app.current_event.json_body.get("where")
    date, time = datetime.utcnow().isoformat().split("T")
    temperature_table.put_item(
        Item={
            "date": date,
            "time": time,
            "where": where,
            "temperature": temperature,
            "humidity": humidity,
        }
    )
    return Response(
        status_code=204,
        body=None,
        content_type="application/json+hal",
    )


@app.exception_handler(Exception)
def handle_exception(ex: Exception):
    exception.handle_exception(ex, app)


def handler(event, context):
    return app.resolve(event, context)
