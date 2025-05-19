from http import HTTPStatus

import flask
from pydantic import ValidationError

from web.tools import entrypoints_registrator

app = flask.Flask(__name__)
entrypoints_registrator.register_routes(app)


@app.errorhandler(ValueError)
def handle_value_error_exception(*args, **kwargs):
    """
    Обработать ошибку Value Error
    """

    return flask.jsonify(
        {
            "code": HTTPStatus.NOT_FOUND,
            "message": "The requested equipment is not found"
        }
    ), HTTPStatus.NOT_FOUND


@app.errorhandler(ValidationError)
def handle_validation_error(*args, **kwargs):
    """
    Обработать ошибку Validation Error
    """

    return flask.jsonify(
        {
            "code": HTTPStatus.BAD_REQUEST,
            "message": "Invalid data"
        }
    ), HTTPStatus.BAD_REQUEST


@app.errorhandler(RuntimeError)
def handle_runtime_error(*args, **kwargs):
    """
    Обработать ошибку Runtime Error
    """

    return flask.jsonify(
        {
            "code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "message": "Internal provisioning exception"
        }
    ), HTTPStatus.INTERNAL_SERVER_ERROR
