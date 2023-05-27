from . import views
from django.urls import path

urlpatterns = [
    path('signup',views.SignUp.as_view(),name='signup'),
    path('login',views.Login.as_view(),name='login'),
    path('manage_friend/', views.ManageFriend.as_view({'get':'get_all_friend','post':'accept_friend_request'})),
    path('create_request/', views.createRequest.as_view({'post':'create_friend_request'})),
    path('get_all_friend/', views.ManageFriend.as_view({'get':'get_pending_accept_friend'})),
]