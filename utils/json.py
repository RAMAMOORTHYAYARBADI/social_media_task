from django.shortcuts import HttpResponse
import json, codecs


def Response(data,message,http_code,error=True, json_format=True):
    if error:
        status = True
        response = {
            "data": data,
            "message":message,
            "status": status,
            "http_code": http_code
        }
        # http_code=200
    else:
        status = False
        # http_code=404
        response = {
            "data": data,
            "message":message,
            "status": status,
            "http_code":http_code
        }
    if json_format:
        response = json.dumps(response)

    return HttpResponse(response, content_type='Application/json', status=int(http_code))
