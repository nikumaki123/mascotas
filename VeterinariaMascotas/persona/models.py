from django.db import models
from django.contrib import admin


# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


#Modelo tipo de animal
class TipoAnimal(models.Model):
    nombreTipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreTipo

#Modelo de animal
class Animal(models.Model):
    idTipoAnimal = models.CharField(max_length=50)
    idDueno = models.ForeignKey(Persona, on_delete = models.CASCADE, null = True)
    nombreAnimal = models.CharField(max_length=50)
    fechaNacimiento = models.DateField('Fecha de Nacimiento')
    raza = models.CharField(max_length=50)
    sexo = models.CharField(max_length=50)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField()
    imagen = models.ImageField(upload_to='animal_images/', null=True, blank=True)

    def __str__(self):
        return self.nombreAnimal


    
class Medicina(models.Model):
    nombreMedicamento = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreMedicamento


class Consulta(models.Model):
    idAnimal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    sintomas = models.TextField()
    observaciones = models.TextField()
    diagnostico = models.TextField()
    fechaConsulta = models.DateField('Fecha Consulta:', null=True)
    receta = models.ManyToManyField(Medicina, through='Medicacion')


class Medicacion(models.Model):
    medicina = models.ForeignKey(Medicina, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)

class MedicacionInLine(admin.TabularInline):
    model = Medicacion
    extra = 1

class ConsultaAdmin(admin.ModelAdmin):
    inlines = (MedicacionInLine,)

class MedicinaAdmin(admin.ModelAdmin):
    inlines = (MedicacionInLine,)


    


