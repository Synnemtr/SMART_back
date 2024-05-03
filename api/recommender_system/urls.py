from django.urls import path
from api.recommender_system.views import RecommendationView


urlpatterns = [
    path("user/", RecommendationView.as_view({'get': 'list'})),
]
