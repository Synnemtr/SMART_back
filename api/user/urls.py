from django.urls import path
from api.user.views import (
    UserDetail,
    GetUserList,
    CreateUserList,
    ProfileDetail,
    ProfileList
)

urlpatterns = [
    path("<int:pk>/", UserDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("", GetUserList.as_view({'get': 'list'})),
    path("add/", CreateUserList.as_view({'post': 'create'})),
    path("profile/<int:pk>/", ProfileDetail.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("profile/add/", ProfileList.as_view({'post': 'create'}))
]
