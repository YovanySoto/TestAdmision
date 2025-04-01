from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
import requests
from django.core.paginator import Paginator
from django.conf import settings
from requests.exceptions import RequestException
from .models import UserProfile
from .forms import CustomRegisterForm
from .services import crear_usuario
from .data.juegos import juegos

def index(request):
    context = {'productos': juegos}
    messages.success(request, "¡Este es un mensaje de prueba!")
    return render(request, 'index.html', context)

class RegisterView(View):
    def get(self, request):
        form = CustomRegisterForm()
        return render(request, 'registration/register.html', {'form': form})
    
    def post(self, request):
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            try:
                success = crear_usuario(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1']
                )
                
                if success:
                    messages.success(request, 'Registro exitoso! Por favor inicia sesión')
                    return redirect('login')
                messages.error(request, 'Error al crear el usuario')
            except Exception as e:
                messages.error(request, f'Error en el registro: {str(e)}')
        
        return render(request, 'registration/register.html', {'form': form})

def games(request):
    if not hasattr(settings, 'RAWG_API_KEY') or not settings.RAWG_API_KEY:
        return render(request, 'games/games.html', {
            'error': 'Configuración de API no disponible',
            'games': None
        })

    try:
        params = {
            'key': settings.RAWG_API_KEY,
            'page_size': 20,
            'ordering': '-rating',
            'search': request.GET.get('search', '')[:100],
            'platforms': request.GET.get('platform', '')[:50],
        }
        
        response = requests.get(
            "https://api.rawg.io/api/games",
            params=params,
            timeout=10
        )
        response.raise_for_status()
        
        paginator = Paginator(response.json().get('results', []), 10)
        
        context = {
            'games': paginator.get_page(request.GET.get('page')),
            'search_query': params['search'],
        }
        
    except RequestException as e:
        context = {
            'games': None,
            'error': f"Error al conectar con RAWG: {str(e)}",
        }
    
    return render(request, 'games/games.html', context)

def games_detalles(request, game_id):
    if not hasattr(settings, 'RAWG_API_KEY'):
        return render(request, 'games/games_detalles.html', {
            'error': 'Configuración de API no disponible',
            'game': None,
            'screenshots': []
        })

    try:
        if not str(game_id).isdigit():
            raise ValueError("ID de juego inválido")
            
        game_response = requests.get(
            f"https://api.rawg.io/api/games/{game_id}",
            params={'key': settings.RAWG_API_KEY},
            timeout=10
        )
        game_response.raise_for_status()
        
        context = {
            'game': game_response.json(),
            'screenshots': [],
        }
        
        screenshots_response = requests.get(
            f"https://api.rawg.io/api/games/{game_id}/screenshots",
            params={'key': settings.RAWG_API_KEY},
            timeout=10
        )
        if screenshots_response.status_code == 200:
            context['screenshots'] = screenshots_response.json().get('results', [])
        
    except (RequestException, ValueError) as e:
        context = {
            'game': None,
            'screenshots': [],
            'error': f"Error al obtener detalles: {str(e)}",
        }
    
    return render(request, 'games/games_detalles.html', context)