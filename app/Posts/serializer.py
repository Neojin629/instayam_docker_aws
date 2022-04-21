from rest_framework import serializers
from Posts.models import Posts
from django import forms


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class PostValidator(forms.Form):
    username = forms.CharField()
    content_text = forms.CharField()


class ReplyValidator(forms.Form):
    username = forms.CharField()
    reply_text = forms.CharField()


class SharedPostValidator(forms.Form):
    username = forms.CharField()
