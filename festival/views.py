from django.shortcuts import render, redirect
from .forms import UsuarioForm
from .models import Usuario
from .models import Voto, Categoria, Opcion, Edicion
from .forms import VotoForm
from django.db.models import Count
from django.http import JsonResponse

def inicio(request):

            if 'usuario_id' not in request.session:
                return redirect('login')

            usuario = Usuario.objects.get(
                id=request.session['usuario_id']
            )

            return render(
                request,
                'inicio.html',
                {
                    'usuario': usuario
                }
            )

def index(request):
            return render(request, 'index.html')

def registro(request):

            if request.method == 'POST':

                correo = request.POST['correo']

            if Usuario.objects.filter(correo=correo).exists():

                    return render(
                        request,
                        'registro.html',
                        {
                            'formulario': UsuarioForm(),
                            'mensaje': 'El correo ya se encuentra registrado'
                        }
                    )

            formulario = UsuarioForm(request.POST)

            if formulario.is_valid():

                    formulario.save()

                    return redirect('login')

            formulario = UsuarioForm()

            return render(
                request,
                'registro.html',
                {
                    'formulario': formulario
                }
            )

def login(request):

            mensaje = ""

            if request.method == 'POST':

                correo = request.POST['correo']
                password = request.POST['password']

                try:

                    usuario = Usuario.objects.get(
                        correo=correo,
                        password=password
                    )

                    request.session['usuario_id'] = usuario.id

                    return redirect('inicio')

                except Usuario.DoesNotExist:

                    mensaje = "Usuario o contraseña incorrectos"

            return render(
                request,
                'login.html',
                {
                    'mensaje': mensaje
                }
            )

def votar(request, categoria_id):

            mensaje = ""

            categoria = Categoria.objects.get(
                id=categoria_id
                
            )

            if not categoria.habilitada:

                return render(
                    request,
                    'votacion.html',
                    {
                        'categoria': categoria,
                        'opciones': [],
                        'mensaje': 'La categoría seleccionada no está habilitada para votación.'
                    }
                )

            opciones = Opcion.objects.filter(
                categoria=categoria
            )

            if request.method == 'POST':

                usuario = Usuario.objects.get(
            id=request.session['usuario_id']
                )

                opcion_id = request.POST['opcion']

                opcion = Opcion.objects.get(
                    id=opcion_id

                )

                if opcion.categoria != categoria:

                    return render(
                request,
                'votacion.html',
                {
                    'categoria': categoria,
                    'opciones': opciones,
                    'mensaje': 'La opción seleccionada no pertenece a esta categoría.'
                }
                )

                edicion = categoria.edicion

                existe_voto = Voto.objects.filter(
                    usuario=usuario,
                    categoria=categoria,
                    edicion=edicion
                ).exists()

                if existe_voto:

                    mensaje = "Ya votaste en esta categoría"

                else:

                    Voto.objects.create(
                        usuario=usuario,
                        categoria=categoria,
                        edicion=edicion,
                        opcion=opcion
                    )

                    mensaje = "Voto registrado correctamente"

            return render(
                request,
                'votacion.html',
                {
                    'categoria': categoria,
                    'opciones': opciones,
                    'mensaje': mensaje
                }
            )

def categorias_votacion(request):

            if 'usuario_id' not in request.session:
                return redirect('login')

            categorias = Categoria.objects.all()

            return render(
                request,
                'categorias_votacion.html',
                {
                    'categorias': categorias
                }
            )

def mis_votos(request):

            if 'usuario_id' not in request.session:
                return redirect('login')

            usuario = Usuario.objects.get(
            id=request.session['usuario_id']
            )

            votos = Voto.objects.filter(
                usuario=usuario
            )

            return render(
                request,
                'mis_votos.html',
                {
                    'votos': votos
                }
            )

def resultados(request):

            if 'usuario_id' not in request.session:
                    return redirect('login')
            

            categorias = Categoria.objects.all()

            resultados = []

            for categoria in categorias:

                opciones = (
                    Opcion.objects
                    .filter(categoria=categoria)
                    .annotate(total_votos=Count('voto'))
                    .order_by('-total_votos')
                )

                resultados.append({
                    'categoria': categoria,
                    'opciones': opciones
                })

            return render(
                request,
                'resultados.html',
                {
                    'resultados': resultados
                }
            )

def logout(request):

            request.session.flush()

            return redirect('login')

def api_categorias(request):

            categorias = Categoria.objects.all()

            datos = []

            for categoria in categorias:

                opciones = Opcion.objects.filter(
                    categoria=categoria
                )

                datos.append({
                    'categoria': categoria.nombre,
                    'opciones': [
                        opcion.nombre
                        for opcion in opciones
                    ]
                })

            return JsonResponse(
                datos,
                safe=False
)