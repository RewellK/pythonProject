from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .controller import Controller
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

def address_request(request):
    if request.method == 'POST':

        # processar os dados do formulário
        pass
    else:
        # exibir o formulário vazio
        return render(request, 'address_request.html')


def process_addresses(request):
    if request.method == 'POST':
        controller = Controller()
        num_addresses = int(request.POST.get("num_addresses"))
        for i in range(num_addresses):
            str_street = request.POST.get(f"str_street_{i}")
            str_number = request.POST.get(f"str_number_{i}")
            str_city = request.POST.get(f"str_city_{i}")
            str_state = request.POST.get(f"str_state_{i}")
            str_cep = request.POST.get(f"str_cep_{i}")
            controller.addAddress(str_street, str_number, str_city, str_state, str_cep)

        ordered_addresses = controller.processAddresses()

        return render(request, 'address_return.html', {'ordered_addresses': ordered_addresses})

    return redirect('guias:locator')

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Process the login form
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('guias:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('guias:login')

def locator(request):
    return render(request, 'locator.html')

def address_return(request):
    ordered_addresses = []  # Coloque aqui a lista ordenada de endereços
    return render(request, 'address_return.html', {'ordered_addresses': ordered_addresses})
