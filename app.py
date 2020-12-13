import os
import sys
import copy
import json


import logging
from datetime import datetime


from flask import Flask, Response
from flask import request
import flask

"""
import middleware.context as context
import middleware.security as sec
import middleware.notification as notify
"""

from CustomerService.user_service.UserService import UserService

# DFF TODO
_default_limit = 10


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)

_user_service = UserService()

def initialize():
    global _users_svc

    _user_svc = UserService()


initialize()

##################################################################################################################

def _get_and_remove_arg(args, arg_name):

    val = copy.copy(args.get(arg_name, None))
    if val is not None:
        del args[arg_name]

    return args, val


def _de_array_args(args):

    result = {}

    if args is not None:
        for k,v in args.items():
            if type(v) == list:
                result[k] = ",".join(v)
            else:
                result[k] = v

    return result


# 1. Extract the input information from the requests object.
# 2. Log the information
# 3. Return extracted information.
#
def log_and_extract_input(method, path_params=None):

    path = request.path
    args = dict(request.args)
    args = _de_array_args(args)
    data = None
    headers = dict(request.headers)
    method = request.method

    args, limit = _get_and_remove_arg(args, "limit")
    args, offset = _get_and_remove_arg(args, "offset")
    args, order_by = _get_and_remove_arg(args, "order_by")
    args, fields = _get_and_remove_arg(args, "fields")

    if limit is None:
        limit = _default_limit

    try:
        if request.data is not None:
            data = request.json
        else:
            data = None
    except Exception as e:
        # This would fail the request in a more real solution.
        data = "You sent something but I could not get JSON out of it."

    log_message = str(datetime.now()) + ": Method " + method

    inputs =  {
        "path": path,
        "method": method,
        "path_params": path_params,
        "query_params": args,
        "headers": headers,
        "body": data,
        "limit": limit,
        "offset": offset,
        "order_by": order_by,
        "url": request.url,
        "base_url": request.base_url,
        "fields": fields
        }

    log_message += " received: \n" + json.dumps(inputs, indent=2)
    logger.debug(log_message)

    return inputs


def log_response(method, status, data, txt):

    msg = {
        "method": method,
        "status": status,
        "txt": txt,
        "data": data
    }

    logger.debug(str(datetime.now()) + ": \n" + json.dumps(msg, indent=2, default=str))


# This function performs a basic health check. We will flesh this out.
@app.route("/health", methods=["GET"])
def health_check():

    rsp_data = { "status": "healthy", "time": str(datetime.now()) }
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="app/json")
    return rsp


@app.route("/api/demo/<parameter>", methods=["GET", "POST"])
def demo(parameter):

    inputs = log_and_extract_input(demo, { "parameter": parameter })

    msg = {
        "/demo received the following inputs" : inputs
    }

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp


@app.route("/api/users/<email>", methods=["GET", "DELETE", "PUT"])
def get_by_email(email):
    inputs = log_and_extract_input(demo, {"parameter": email})

    msg = {
        "/demo received the following inputs": inputs
    }

    if inputs["method"] == "GET":
        res = _user_service.get_by_id(email)

    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route("/")
def hello():
    return "Hello, World!"




#if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=8000)



