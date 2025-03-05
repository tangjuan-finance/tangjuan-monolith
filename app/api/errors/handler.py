from werkzeug.exceptions import HTTPException
from app.api import bp
from flask import jsonify
import datetime
from app.api.errors.base import BaseCustomHTTPException


# Specific HTTP Exception
@bp.errorhandler(BaseCustomHTTPException)
def handle_custom_error(e):
    return jsonify(e.to_dict()), e.code


# General HTTP Exception
@bp.errorhandler(HTTPException)
def handle_http_exception(e):
    response = {
        "status": "error",
        "statusCode": e.code,
        "error": {
            "code": e.name,
            "message": e.description or "",
            "timestamp": datetime.datetime.now(),
        },
    }
    return jsonify(response), e.code


# 500: Server Exception
@bp.errorhandler(Exception)
def handle_generic_exception(e):
    response = {
        "status": "error",
        "statusCode": 500,
        "error": {
            "code": "InternalServerError",
            "timestamp": datetime.datetime.now(),
        },
    }
    return jsonify(response), 500
