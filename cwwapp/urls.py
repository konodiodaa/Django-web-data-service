from django.urls import path
from cwwapp import views

urlpatterns = [
    path('api/login/', views.login),
    path('api/logout/',views.logout),
    path('api/poststory/',views.poststory),
    path('api/getstories/',views.getStories),
    path('api/deletestory/',views.deleteStory)
]