from rest_framework.response import Response
from rest_framework import status

def ok(data=None, status=status.HTTP_200_OK):
    return Response(data, status=status)

def created(data=None):
    return ok(data, status=status.HTTP_201_CREATED)

def no_content():
    return Response(status=status.HTTP_204_NO_CONTENT)