from django.shortcuts import redirect

def redirect_home(request):
    response = redirect('/accounts/')
    return response