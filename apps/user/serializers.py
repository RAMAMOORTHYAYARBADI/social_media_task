from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields  =('id','user_name','email','phone_number','gender','profile_picture','created_at')
        
    
class FriendRequestSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        obj2 = Profile.objects.filter(id=instance.recipient_id).last()
        data['Friend_data'] = UserSerializer(obj2).data
        return data
    class Meta:
        model = FriendRequest
        fields ='__all__'
        
class FriendSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        obj2 = Profile.objects.filter(id=instance.friend_id).last()
        data['Friend_data'] = UserSerializer(obj2).data
        return data
    class Meta:
        model = Friend
        fields ='__all__'