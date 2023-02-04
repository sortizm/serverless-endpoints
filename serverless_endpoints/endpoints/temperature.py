import json
import os
from datetime import datetime

import boto3
from aws_lambda_powertools.event_handler.api_gateway import Response

from serverless_endpoints import app

temperature_table = boto3.resource(
    "dynamodb", region_name=os.getenv("AWS_REGION", "eu-west-1")
).Table("serverless-endpoints.temperature")


@app.post("/temperature/log")
def log_temperature() -> Response:
    temperature = app.current_event.json_body["temperature"]
    humidity = app.current_event.json_body.get("humidity")
    where = app.current_event.json_body.get("where")
    date, time = datetime.utcnow().isoformat().split("T")
    entry = {
        "date": date,
        "time": time,
        "where": where,
        "temperature": temperature,
        "humidity": humidity,
    }
    temperature_table.put_item(Item=entry)
    return Response(
        status_code=201,
        body=json.dumps(entry),
        content_type="application/json",
    )
