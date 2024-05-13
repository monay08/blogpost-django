from django.urls import path
from . import views
from .views import Home, Detail, Create, Update, Delete, Likes, AddComment, Featured

urlpatterns = [
    path('', Featured.as_view(), name='home'),
    path('detail/<int:pk>', Detail.as_view(), name='blogdetail'),
    path('addpost/', Create.as_view(), name='createpost'),
    path('detail/update/<int:pk>', Update.as_view(), name='updatepost'),
    path('detail/<int:pk>/delete', Delete.as_view(), name='deletepost'),
    path('like/<int:pk>', Likes, name='like_post'),
    path('detail/<int:pk>/comment/', AddComment.as_view(), name='addcomment'),
    path('all/', Home.as_view(), name='all'),
]