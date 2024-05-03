from django.urls import path
from api.recommender_rating.views import RatingList

urlpatterns = [
    path('', RatingList.as_view({'get': 'list', 'post': 'create'})),
]
