from django.shortcuts import render, redirect
from .models import Product

def tablaProductos(request):
    products = Product.objects.all()
    return render(request, 'prueba.html', {'products': products})

def guardarProductos(request):
    print(request.POST)
    objeto = Product(
        name=request.POST.get('nombre'),
        unitPrice=request.POST.get('precio'),
        quantity=request.POST.get('cantidad'),
        limitDate=request.POST.get('limit_date')
        # Agrega aquí los campos para las demás categorías
    )
    objeto.save()

    # Aquí puedes guardar los datos en la base de datos o realizar cualquier otra acción que necesites.

    return redirect('prueba')  # Redirige a la vista llamada 'prueba', que es la vista de tablaProductos.
