import json
import os
import sys
import traceback
import time

# flask dependency
from flask import Flask, request, make_response


# dto dependency


# ----------------------------------------------initial----------------------------------------------
# main application
app = Flask(__name__)

# ---------------------------------------------- functions ----------------------------------------------

# ----------------------------------------------routers----------------------------------------------

@app.route("/record_metric", methods=["POST"])
def process():
    try:
        data = request.get_json()
        print(data)
        

    except Exception as e:
        traceback.print_exc()
    
    res = {"code":200,"message":"","data":None}
    response = make_response(json.dumps(res, ensure_ascii=False))
    response.headers["Content-Type"] = "application/json;charset=UTF-8"
    return response

@app.route("/record_metric2", methods=["GET"])
def process2():
    try:
        name = request.args.get("name")
        value = request.args.get("value")
        print(name)
        print(value)
        

    except Exception as e:
        traceback.print_exc()
    
    res = {"code":200,"message":"","data":None}
    response = make_response(json.dumps(res, ensure_ascii=False))
    response.headers["Content-Type"] = "application/json;charset=UTF-8"
    return response


# ----------------------------------------------main----------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
