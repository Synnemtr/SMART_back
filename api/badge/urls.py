from django.urls import path
from api.badge.views import (
    BadgeListView,
    BadgeDetailView,
    UserBadgeListView,
    UserBadgeDetailView,
    BadgeEarnedListView,
)

urlpatterns = [
    path("", BadgeListView.as_view({'get': 'list', 'post': 'create'})),
    path("<int:pk>/", BadgeDetailView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path("user/", UserBadgeListView.as_view({'post': 'create'})),
    path("user/<int:pk>/", UserBadgeDetailView.as_view({'delete': 'destroy'})),
    path("earned/", BadgeEarnedListView.as_view({'get': 'list'}))
]
