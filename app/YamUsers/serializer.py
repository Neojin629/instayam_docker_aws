from rest_framework import serializers
from YamUsers.models import YamUser


class YamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YamUser
        fields = '__all__'
