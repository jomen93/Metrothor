from django.contrib import admin
from Catalogo.models import diametro, TipoMaterial, Tornillo,Existencia

admin.site.register(Tornillo)
admin.site.register(diametro)
admin.site.register(TipoMaterial)
admin.site.register(Existencia)

