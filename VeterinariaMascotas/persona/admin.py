from django.contrib import admin
from .models import Persona, TipoAnimal, Animal, Consulta, Medicina, Medicacion, ConsultaAdmin, MedicinaAdmin

# Register your models here.
admin.site.register(Persona)
admin.site.register(TipoAnimal)
admin.site.register(Animal)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Medicina, MedicinaAdmin)

