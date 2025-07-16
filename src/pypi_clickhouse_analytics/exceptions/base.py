from starlette import status


class BaseError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
