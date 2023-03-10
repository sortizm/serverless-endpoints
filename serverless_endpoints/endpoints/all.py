import json
from logging import Logger

from aws_lambda_powertools.event_handler.api_gateway import Response
from aws_lambda_powertools.event_handler.exceptions import NotFoundError

from serverless_endpoints import app
from serverless_endpoints.logger import get_logger


@app.exception_handler(Exception)
def handle_exception(ex: Exception):
    metadata = {"path": app.current_event.path}
    logger: Logger = get_logger()
    logger.info(metadata)
    if isinstance(ex, NotFoundError):
        logger.error(
            f"Not found: {app.current_event.http_method} - {app.current_event.path}"
        )
        return Response(
            status_code=404,
            content_type="application/json",
            body=None,
        )
    else:
        error_response = {
            "error_name": ex.__class__.__name__,
            "error_description": str(ex),
        }

        return Response(
            status_code=500,
            content_type="application/json",
            body=json.dumps(error_response),
        )


def handler(event, context):
    import serverless_endpoints.endpoints.temperature  # noqa

    return app.resolve(event, context)
