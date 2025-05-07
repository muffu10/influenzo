from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .data import media_data                    #import the list to be computed from data.py


def home(request):
    return render(request, 'home.html')         #To be shown on the home page

def get_sum(media):
    return media["like_count"] + media["comment_count"]       #Return Sum

@api_view(['GET'])
def unsorted_data(request):
    return Response(media_data)                               #To Return Unsorted(Original) Data

def precompute(media_data):                                   #Precomputing values, so we dont have to call again and again
    for media in media_data:
        media['like_count']=int(media["like_count"])          #Converting to int for sorting
        media['comment_count']=int(media['comment_count'])

precompute(media_data)

@api_view(['GET'])
def sorted_data(request):                                     #To return sorted data
    try:

        sorted_media = sorted(media_data, key=get_sum, reverse=True)       #Used Inbuilt sorting of python (TimSort- Time Complexity: O(nlogn))

        return Response(sorted_media)                                   

    except Exception as e:                                                 #Exception handling
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       #Returns the status code in case of error
