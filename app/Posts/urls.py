from django.urls import path
from . import views

urlpatterns = [
    path('create', views.CreatePost),
    path('<str:username>/', views.Timeline),
    path('<int:post_id>/delete', views.DeletePost),
    path('<int:post_id>', views.ShowPost),
    path('<int:post_id>/reply', views.Reply),
    path('<int:post_id>/share', views.Share),
    path('<int:post_id>/like', views.Like),
    path('search', views.Search),
    path('all_posts', views.all_posts),
]
