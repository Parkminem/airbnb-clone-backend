from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("amenities/", views.Amenities.as_view()),
    path("amenities/<int:pk>", views.AmenitiesDetail.as_view()),
]
