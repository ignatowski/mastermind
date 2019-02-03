from mastermind_api import views
from django.urls import path



urlpatterns = [
    path('games/', views.GameCreate.as_view(), name='game-create'),
    path('games/<int:pk>/', views.GameDetails.as_view(), name='game-details'),
    path('moves/', views.MoveCreate.as_view(), name='move-create'),
]
