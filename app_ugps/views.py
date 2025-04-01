from django.shortcuts import render, redirect
from django.contrib import messages
from app_ugps.data.juegos import juegos
from django.views import View
from django.contrib.auth.models import User
import requests
from .models import UserProfile
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from .services import crear_usuario
from .forms import CustomRegisterForm  # Formulario personalizado que crearemos
# Create your views here.

	
def index(request):
	context = {
		'productos': juegos
    }
	messages.success(request, "¡Este es un mensaje de prueba!")
	return render(request, 'index.html', context)

""" class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()  # Usamos el formulario incorporado de Django
        return render(request, 'registration/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Crear perfil
            UserProfile.objects.create(
                user=user,
                tipo='cliente'
            )
            
            messages.success(request, 'Registro exitoso! Por favor inicia sesión')
            return redirect('login')  # Asegúrate de tener esta URL configurada
        
        # Si el formulario no es válido, mostrar errores
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return render(request, 'app_ugps/register.html', {'form': form}) """

class RegisterView(View):
    def get(self, request):
        form = CustomRegisterForm()  # Usamos nuestro formulario personalizado
        return render(request, 'registration/register.html', {'form': form})
    
    def post(self, request):
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            # Extraemos los datos del formulario
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            try:
                # Usamos nuestra función personalizada
                success = crear_usuario(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                
                if success:
                    messages.success(request, 'Registro exitoso! Por favor inicia sesión')
                    return redirect('login')
                else:
                    messages.error(request, 'Error al crear el usuario')
            
            except Exception as e:
                messages.error(request, f'Error en el registro: {str(e)}')
        
        # Si el formulario no es válido o hubo error
        return render(request, 'app_ugps/register.html', {'form': form})

def games(request):
    api_key = settings.RAWG_API_KEY  # Guarda tu API key en settings.py
    base_url = "https://api.rawg.io/api/games"
    
    # Parámetros de búsqueda (personalizables desde la URL)
    params = {
        'key': api_key,
        'page_size': 20,
        'ordering': '-rating',  # Ordenar por rating descendente
        'search': request.GET.get('search', ''),  # Búsqueda por nombre
        'platforms': request.GET.get('platform', ''),  # Filtro por plataforma
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Paginación
        paginator = Paginator(data['results'], 10)  # 10 juegos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
    except requests.RequestException as e:
        page_obj = None
        error_message = f"Error al conectar con RAWG: {str(e)}"
    
    context = {
        'games': page_obj,
        'error': error_message if 'error_message' in locals() else None,
        'search_query': params['search'],
    }
    return render(request, 'games/games.html', context)

def games_detalles(request, game_id):
    api_key = settings.RAWG_API_KEY
    url = f"https://api.rawg.io/api/games/{game_id}"
    
    try:
        response = requests.get(url, params={'key': api_key})
        response.raise_for_status()
        game = response.json()
        
        # Obtener screenshots
        screenshots_url = f"{url}/screenshots"
        screenshots = requests.get(screenshots_url, params={'key': api_key}).json().get('results', [])
        
    except requests.RequestException as e:
        game = None
        screenshots = []
        error_message = f"Error al obtener detalles: {str(e)}"
    
    context = {
        'game': game,
        'screenshots': screenshots,
        'error': error_message if 'error_message' in locals() else None,
    }
    return render(request, 'games/games_detalles.html', context)

