from configs.config import ApplicationConfig
from context import Context
from transport.flask import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> tuple:
    return (
        endpoints.HealthEndpoint(
            config=config, context=context, uri='/', methods=['GET']
        ),
        # endpoints.ProcessingVideoEndpoint(
        #     config=config, context=context, uri='/processing/video', methods=['GET', 'POST']
        # ),
        # endpoints.CancelProcessingVideoEndpoint(
        #     config=config, context=context, uri='/processing/video/<id:int>/cancel', methods=['POST']
        # ),
    )
