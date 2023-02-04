from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, CORSConfig

cors_config = CORSConfig()
app = APIGatewayHttpResolver(cors=cors_config)
