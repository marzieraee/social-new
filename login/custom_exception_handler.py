from rest_framework.views import exception_handler
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied,MethodNotAllowed,NotAcceptable,UnsupportedMediaType
from rest_framework.response import Response


def custom_exception_handler(exc, context):
  '''it class handle the known exceptions 
  '''
    
   
    response = exception_handler(exc, context)


    if isinstance(exc, AuthenticationFailed):  
        return Response({"detail": "لطفا ابتدا وارد سایت شوید"}, status=401)
    elif isinstance(exc, PermissionDenied):  
        return Response({"detail": "اجازه دسترسی ندارید"}, status=403)
    elif isinstance(exc, Http404):  
        return Response({"detail": "موردی یافت نشد"}, status=404)
    elif isinstance(exc, MethodNotAllowed):  
        return Response({"detail": "اجازه اجرای این در خواست را ندارید"}, status=405)
    elif isinstance(exc, NotAcceptable):  
        return Response({"detail": "فرمت ارسال شده قابل قبول نیست"}, status=406)
   
   
    return exception_handler(exc, context)
   
