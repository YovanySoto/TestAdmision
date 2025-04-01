from django.contrib import admin
from app_ugps.models import UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)
# Modificación de títulos en el Django Admin (opcional)
admin.site.site_header = "Titulo"
admin.site.index_title = "Bienvenidos al portal de administración de Juegos UGPS"
