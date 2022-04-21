from datetime import datetime
from YamUsers.models import YamUser
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from Posts.models import Posts
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Posts.serializer import PostSerializer, PostValidator, SharedPostValidator, ReplyValidator
from django.core.paginator import Paginator
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


def get_user_obj(user=None):
    # Returns User Objects corresponding to the username
    return YamUser.objects.get(username=user)


@api_view(['POST'])
def CreatePost(request):
    '''
    Purpose: Creates a new Post
    Input: 
    username: (mandatory) <str> Account user
    post_text: (mandatory) <str> Post
    Output: Post Object of the created post
    '''
    if request.method == "POST":
        username = request.query_params.get('username')
        text = request.query_params.get('content_text')
        validate = PostValidator(request.query_params, request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Invalid username or content_text"}
            logger.error(error)
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_obj(username)
            new_content = Posts(username=user, content_text=text)
            new_content.save()
            serializer = PostSerializer(new_content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "User Does not exist"}
            logger.error(e)
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def Timeline(request, username):
    '''
    Purpose: Returns the Timeline of the User in a Paginated Fashion
    Input: page (mandatory) <int>  
    Output: Post object with all the Posts in the page
    '''
    if (request, username):
        try:
            page_no = int(request.query_params.get('page', 1))
            userObj = get_user_obj(username)
            if page_no < 1:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                         'Error_Message': "Please pass an integer value (starting with 1) as Page Number"}
                logger.error(error)
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

            posts = Posts.objects.filter(username=userObj)
            paginator = Paginator(posts, 5)  # shows 5 posts per page
            page_num = paginator.get_page(page_no)
            post_objs = page_num.object_list
            serializer = PostSerializer(post_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "No Posts to show"}
            logger.error(e)
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def DeletePost(request, post_id=None):
    '''
    Purpose: Deletes the post having the id in the URL
    Input: None  
    Output: Post object that was deleted
    '''
    try:
        post = Posts.objects.get(id=post_id)
        username = post.username.username
        if (request, username):
            serializer = PostSerializer(post)
            post.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "This post no longer exists"}
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ShowPost(request, post_id=None):
    '''
    Purpose: displays the post with the id in the URL and its replies
    Input: None  
    Output: Posts and its replies
    '''
    try:
        post = Posts.objects.filter(id=post_id)
        username = post.username.username
        if (request, username):
            replies = Posts.objects.get(id=post_id).reply.all()
            postNreply = post.union(replies)
            serializer = PostSerializer(postNreply, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(e)
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "This post no longer exists"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def Reply(request, post_id=None):
    '''
    Purpose: Reply to the post with the id in the URL
    Input: username (mandatory) <str> Account user
           reply_text (mandatory) <str> Reply  
    Output: Replied post object
    '''
    try:
        user = request.query_params.get('username', None)
        reply = request.query_params.get('reply_text', None)
        validate = ReplyValidator(request.query_params, request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Invalid username or reply_text"}
            logger.error(error)
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        if (request, user):
            user = get_user_obj(user)
            reply_post = Posts(username=user, post_text=reply)
            reply_post.save()
            post = Posts.objects.get(id=post_id)
            post.reply.add(reply_post)
            post.save()
            serializer = PostSerializer(reply_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Error saving the reply"}
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def Share(request, post_id=None):
    '''
    Purpose: Share the post with the id in the URL
    Input: username (mandatory) <str> Account user
           comment (optional) <str> Comment  
    Output: post object with comment
    '''
    try:
        user = request.query_params.get('username', None)
        comment = request.query_params.get('comment', None)
        validate = SharedPostValidator(request.query_params, request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Invalid username"}
            logger.error(error)
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

        if (request, user):
            post_text = Posts.objects.get(id=post_id).post_text
            reply_post = Posts(username=get_user_obj(
                user), post_text=post_text, comment=comment)
            reply_post.save()
            post = Posts.objects.get(id=post_id)
            post.share.add(get_user_obj(user))
            post.save()
            serializer = PostSerializer(reply_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Error sharing!"}
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def Like(request, post_id=None):
    '''
    Purpose: Like the post with the id in the URL
    Input: username (mandatory) <str> Account user 
    Output: post object that was liked
    '''
    try:
        user = request.query_params.get('username', None)
        validate = SharedPostValidator(request.query_params, request.FILES)
        if not validate.is_valid():
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Invalid username"}
            logger.error(error)
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

        if (request, user):
            post = Posts.objects.get(id=post_id)
            post.like.add(get_user_obj(user))
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Error liking the post!"}
        logger.error(e)
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def Search(request):
    '''
    Search for a post using a hashtag and a region
    Input:
    username <str> (mandatory) Account User
    hashtag <str> (mandatory) text (with hashtag) to search with
    '''
    user = request.query_params.get('username')
    hashtag = request.query_params.get('hashtag')
    if (request, user):
        try:
            post_match = Posts.objects.filter(
                post_text__contains=hashtag[1:])
            if post_match:
                serializer = PostSerializer(post_match, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                message = {"Message": "No Match found!"}
                return Response(message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error = {'Error_code': status.HTTP_204_NO_CONTENT,
                     'Error_Message': "Please enter a valid search string"}
            logger.error(e)
        return Response(error, status=status.HTTP_204_NO_CONTENT)
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_posts(request):
    '''
    Shows all posts
    '''
    posts = Posts.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
