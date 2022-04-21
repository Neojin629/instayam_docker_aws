from django.db import models
from YamUsers.models import YamUser
from datetime import datetime

get_cur_time = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')


class Posts(models.Model):
    username = models.ForeignKey(YamUser, on_delete=models.CASCADE)
    content_text = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=50, default=get_cur_time)
    shared = models.ManyToManyField(YamUser, related_name="shared_users")
    like = models.ManyToManyField(YamUser, related_name="liked_users")
    reply = models.ManyToManyField("self")
    comment = models.CharField(max_length=100, null=True)
