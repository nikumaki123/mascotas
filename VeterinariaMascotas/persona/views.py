from django.shortcuts import render, get_object_or_404, redirect
from persona.models import Persona, Animal, Consulta, Medicina, Medicacion
from .forms import PersonaForm, AnimalForm, ConsultaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .forms import RegistrationForm
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny

from .models import MyUser
from .serializers import MyUserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def obtener_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Se requieren los campos "username" y "password".'}, status=400)

    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        return Response({'error': 'Credenciales inválidas.'}, status=400)

    if not user.check_password(password):
        return Response({'error': 'Credenciales inválidas.'}, status=400)

    # Generar tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        'access_token': access_token,
        'refresh_token': str(refresh)
    })


class MiVista(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'mensaje': 'Hola, este es un recurso protegido.'}
        return Response(content)


@permission_classes([IsAuthenticated]) # Añade la autenticación requerida
@api_view(['GET', 'POST'])
def posts_list(request):
    if request.method == 'GET':
        books = BlogPost.objects.all()
        serializer = BlogPostSerializer(books, many=True)
    return Response(serializer.data)



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