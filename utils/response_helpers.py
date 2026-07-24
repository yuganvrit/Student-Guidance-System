from rest_framework.response import Response

def success_response(data=None, message="Success", status_code=200):
    response = {
        'success':True,
        'message':message
    }
    if data is not None:
        response['data'] = data
        return Response(response, status=status_code)

    

def error_response(message="Something went wrong",errors=None,  status_code=400):
    response = {
        'message':message,
        'success':False,
    }
    
    if errors is not None :
        response['errors'] = errors
    return Response(response, status=status_code)