from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from YamUsers.models import YamUser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from YamUsers.serializer import YamUserSerializer
import logging
import datetime
from django.conf import settings


logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG,)

EXP_TIME = datetime.timedelta(hours=1)


@api_view(['POST'])
def AccountSignup(request):
    '''
    Purpose: Create a new user
    Input: 
    username (mandatory) <str> Chosen Username 
    password (mandatory) <str> Chosen Password
    Output: User object of the created user
    '''
    data = JSONParser().parse(request)
    serializer = YamUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Login(request, username=None, password=None):
    '''
    Authenticate if username and password is correct. 
    Input
    Output: return User object or Error 
    '''
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    try:
        user = YamUser.objects.get(username=username)
        if user.password == password:
            user.save()
            serializer = YamUserSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Invalid Username or Password"}
            return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Invalid Username"}
        logger.error(e)
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def AccountUpdate(request, username):
    '''
    Purpose: Update Account Details
    Input: 
    username (mandatory) <str> Chosen Username 
    country (optional) <str> Country
    Output: User object of the updated user
    '''
    try:
        country = request.query_params.get('country')
        user = YamUser.objects.get(username=username)
        user.country = country
        user.save()
        serializer = YamUserSerializer(user)
        logger.error("Account Update successful")
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Invalid details"}
        logger.error("AccountUpdate: Error: "+str(e))
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def FollowUser(request, loggedin_user, user):
    '''
    Purpose: Follow the user
    Input: -
    Output: User object of the logged in user
    '''
    try:
        cur_user = YamUser.objects.get(username=loggedin_user)
        fol_user = YamUser.objects.get(username=user)
        cur_user.following.add(fol_user)
        cur_user.save()
        serializer = YamUserSerializer(cur_user)
        return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Request Failed. Invalid Details"}
        logger.error(e)
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetFollowers(request, username):
    '''
    Purpose: Get all the followers for the user
    Input: -
    Output: User object of all the following users
    '''
    try:
        user = YamUser.objects.get(username=username)
        followers = user.followers.all()
        serializer = YamUserSerializer(followers, many=True)
        return JsonResponse(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "User does not exist"}
        logger.error(e)
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def GetFollowing(request, username):
    '''
    Purpose: Get all the users the given user is following
    Input: -
    Output: User object of all the followed users
    '''
    try:
        user = YamUser.objects.get(username=username)
        following = user.following.all()
        serializer = YamUserSerializer(following, many=True)
        return JsonResponse(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "User does not exist"}
        logger.error(e)
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def Block_user(request, username):
    '''
    Purpose: Block the user
    Input: -
    Output: Blocked user
    '''
    try:
        user = YamUser.objects.get(username=username)
        user.blocked = True
        user.save()
        serializer = YamUserSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "User does not exist"}
        logger.error(e)
        return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def users(request):

    if request.method == 'GET':
        users = YamUser.objects.all()
        serializer = YamUserSerializer(users, many=True)
        return JsonResponse(serializer.data)
