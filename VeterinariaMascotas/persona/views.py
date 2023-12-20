from django.shortcuts import render, get_object_or_404, redirect
from .forms import PersonaForm, AnimalForm, ConsultaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .forms import RegistrationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from .models import Persona, Animal, Consulta, Medicina, Medicacion, PersonaSerializer, AnimalSerializer, ConsultaSerializer


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'persona/registro.html', {'form': form})    

@login_required        
def lista_personas(request):
    if request.user.is_active:  # Verifica si el usuario está activo
        personas = Persona.objects.all()
        return render(request, 'persona/lista_personas.html', {'personas': personas})
    else:
        # Redirige a donde desees si el usuario no está activo
        return redirect('persona/registro.html')  # Reemplaza 'pagina_de_inactividad' con el nombre de tu vista o URL

@login_required
def detalle_persona(request, pk):
    if request.user.is_active:  # Verifica si el usuario está activo
        persona = get_object_or_404(Persona, pk=pk)
        return render(request, 'persona/detalle_persona.html', {'persona': persona})
    else:
        # Redirige a donde desees si el usuario no está activo
        return redirect('persona/registro.html')  # Reemplaza 'pagina_de_inactividad' con el nombre de tu vista o URL
@login_required
def persona_new(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona = form.save(commit = False)
            persona.save()
            return redirect('lista_personas')
    else:
        form = PersonaForm()

    return render(request, 'persona/persona_new.html',{'form':form})

@login_required
def persona_edit(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == "POST":
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            persona = form.save(commit = False)
            persona.save()
            return redirect('lista_personas')
    else:
        form = PersonaForm(instance=persona)
        return render(request, 'persona/persona_new.html',{'form':form})

@login_required
def lista_animales(request):
    animales = Animal.objects.all()
    return render(request, 'persona/lista_animales.html', {'animales':animales})

@login_required
def detalle_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'persona/detalle_animal.html',{'animal':animal})

@login_required
def animal_new(request):
    if request.method == "POST":
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit = False)
            animal.save()
            return redirect('lista_animales')
    else:
        form = AnimalForm()
    
    return render(request, 'persona/animal_new.html',{'form':form})

@login_required
def animal_edit(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == "POST":
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            animal = form.save(commit = False)
            animal.save()
            return redirect('lista_animales')
    else:
        form = AnimalForm(instance=animal)
        return render(request, 'persona/animal_new.html',{'form':form})

@login_required
def lista_consultas(request):
    consultas = Consulta.objects.all()
    return render(request, 'persona/lista_consultas.html', {'consultas':consultas})

@login_required
def detalle_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    return render(request, 'persona/detalle_consulta.html',{'consulta':consulta})

@login_required
def consulta_new(request):
    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = Consulta.objects.create(idAnimal=form.cleaned_data['idAnimal'], sintomas=form.cleaned_data['sintomas'], observaciones=form.cleaned_data['observaciones'], diagnostico = form.cleaned_data['diagnostico'], fechaConsulta = form.cleaned_data['fechaConsulta'])
            for medicina_id in request.POST.getlist('receta'):
                medicacion = Medicacion(medicina_id=medicina_id, consulta_id = consulta.id)
                medicacion.save()
            return redirect('lista_consultas')
            
    else:
        form = ConsultaForm()

    return render(request, 'persona/consulta_new.html',{'form':form})

@login_required
def consulta_edit(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit = False)
            consulta.save()
            return redirect('lista_consultas')
    else:
        form = ConsultaForm(instance=consulta)
        return render(request, 'persona/consulta_new.html',{'form':form})

@login_required
def persona_delete(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    persona.delete()
    return redirect('lista_personas')

@login_required
def animal_delete(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    animal.delete()
    return redirect('lista_animales')

@login_required
def consulta_delete(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    consulta.delete()
    return redirect('lista_consultas')


@api_view(['GET', 'POST'])
def personas(request):
    if request.method == 'GET':
        personas = Persona.objects.all()
        serializer = PersonaSerializer(personas, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Vista para obtener detalles de una persona, actualizar o eliminar
@api_view(['GET', 'PUT', 'DELETE'])
def persona_detail(request, pk):
    try:
        persona = Persona.objects.get(pk=pk)
    except Persona.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = PersonaSerializer(persona)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PersonaSerializer(persona, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        persona.delete()
        return Response(status=204)
