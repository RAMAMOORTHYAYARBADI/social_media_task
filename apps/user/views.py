import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics,permissions,status,viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.db import transaction
from .serializers import *
from .models import *
from utils.helper import *
from .throttling import RequestRateThrottle
from utils import permissions as cust_perms 
from utils import validators, json, pagination
from datetime import datetime

logger = logging.getLogger( __name__ )

class SignUp(APIView):
    permission_classes=[permissions.AllowAny]

    """
    User signup API
    """  
    def post(self,request):
        
        try:
            data=request.data
            """check required keys"""
            validate = validators.signup_validator(request)
            if not validate:
                res={'status':False,'message':'datas are missging','data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            if Profile.objects.filter(email = data['email']).exists():
                return json.Response([],"Email is already exists",400,False)
            if data['password'] != data['confirm_password']:
                return json.Response([],"password are mismatched",400,False) 
            data.pop('confirm_password')
            data['date_of_birth'] = datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date()
            data['password'] = make_password(data['password'])       
            Profile.objects.create(**data)
            return json.Response([],"SignedUp Successfully",201,True)
        except Exception as e:
            logger.info(f"{e}: signup error")
            return json.Response([],"Internal Server Error",400,False)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    """
    User Login API
    """ 
    def post(self,request):
        try:
            email = request.data['email']
            password = request.data['password']
            if email == None:
                res = {'status':False,'message':'Kindly Enter The Email','data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            if password == None:
                res = {'status':False,'message':'Kindly Enter The Password','data':[]}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, email=email, password = password)
            if user is not None:
                user = Profile.objects.filter(email=email).last()
                user_data = login_details(user)
                return json.Response(user_data,"Logged In Successfully",200,True)
            else:
                res = {'status':False,'message':'Incorrect Login Details','data':[]}
                return Response(res,status = status.HTTP_400_BAD_REQUEST)           
        except Exception as e:
            logger.info(f"{e}: Login")
            return json.Response([],"Internal Server Error",400,False)
        
class createRequest(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated,cust_perms.Is_User]
    pagination_class = pagination.CustomPagination 
    throttle_classes = [RequestRateThrottle]

    """
    Create 3 friend  request with one minute 
    """ 

    def create_friend_request(self, request):
        try:
            id = request.user.id
            data = request.data 
            if 'status' not in data or 'receiver_id' not in data: return json.Response([],"Required Feild is missing is missing",400,False)
            if data['status'] not in ['REQUESTED']: return json.Response([],"'Invalid Inputs",400,False)
            FriendRequest(sender_id = id,recipient_id =data['receiver_id'],status = data['status']).save()
            return json.Response([],"Friend Requested successfuly",200,True)
        except Exception as e:
            logger.info(f"{e}: create request error")
            return json.Response([],"Internal Server Error",400,False)
        
    
class ManageFriend(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated,cust_perms.Is_User]
    pagination_class = pagination.CustomPagination 

    """
    craete Accept and Reject friend API
    """ 
    def accept_friend_request(self, request):
        try:
            id = request.user.id
            data = request.data 
            if 'status' not in data or 'receiver_id' not in data: return json.Response([],"Required Feild is missing is missing",400,False)
            if data['status'] not in ['ACCEPTED','REJECTED']: return json.Response([],"'Invalid Inputs",400,False)
            FriendRequest(sender_id = id,recipient_id =data['receiver_id'],status = data['status']).save()
            if data['status'] == "ACCEPTED":
                if not Friend.objects.filter(user_id=id,friend_id=data['receiver_id']).exists():
                    Friend(user_id=id,friend_id=data['receiver_id']).save()
                    return json.Response([],"Friend Accepted successfuly",200,True)
                else:
                    return json.Response([],"Aready Friend",400,False)
            if data['status'] == "REJECTED":return json.Response([],"Friend Rejected successfuly",200,True)
        except Exception as e:
            logger.info(f"{e}: accept_friend_request error")
            return json.Response([],"Internal Server Error",400,False)

    """
    Get all friend list API
    """ 
    def get_all_friend(self, request):
        try:
            id = request.user.id
            req_ids=FriendRequest.objects.filter(Q(status="REQUESTED") | Q(status ="ACCEPTED")).values_list('recipient_id',flat=True).distinct()
            queryset = Profile.objects.filter(~Q(id=id) | ~Q(id__in=req_ids)).order_by('-created_at')
            search_query = request.query_params.get('search')
            if search_query:
                queryset = queryset.filter(Q(email=search_query) |
                                        Q(user_name__icontains=search_query))
                
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = UserSerializer(page, many=True)
                return json.Response(paginator.get_paginated_response(serializer.data),"",200,True)

            serializer = UserSerializer(queryset, many=True).data
            return json.Response(serializer,"",200,True)
        except Exception as e:
            logger.info(f"{e}: get_all_friend error")
            return json.Response([],"Internal Server Error",400,False)
    
    """
    Get all pending and accept friend list API
    """ 
    
    def get_pending_accept_friend(self, request):
        try:
            id = request.user.id
            status  = request.query_params.get('status')
            if status.upper() == "REQUESTED":
                obj = FriendRequest.objects.filter(sender_id = id,status ="REQUESTED").order_by('created_at')
                serializer = FriendRequestSerializer(obj,many=True).data
                keys = ["sender", "recipient"]
                data = remove_duplicates(serializer, keys)
                return json.Response(data,"",200,True)

            if status.upper() == "ACCEPTED":
                obj = Friend.objects.filter(user_id =id).order_by('created_at')  
                serializer = FriendSerializer(obj,many=True).data
                return json.Response(serializer,"",200,True)
        except Exception as e:
            logger.info(f"{e}: get_pending_accept_friend error")
            return json.Response([],"Internal Server Error",400,False)

