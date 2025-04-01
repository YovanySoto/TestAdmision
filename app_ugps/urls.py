from app_ugps.services import crear_usuario
from django.urls import path
from app_ugps.views import index, games, games_detalles, RegisterView
urlpatterns = [
    path('', index, name='index'), # Dos comillas para llamar a la ruta raiz /
    path('accounts/registro/', RegisterView.as_view(), name='register'),
    path('games/', games, name='games'),
    path('games/<int:game_id>/', games_detalles, name='game_detail'),
    # path('registro', crear_usuario, name='registro'), 

]


