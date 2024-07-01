from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'edudealio/errors/404.html', status=404)

def custom_500(request):
    return render(request, 'edudealio/errors/500.html', status=500)

def custom_504(request):
    return render(request, 'edudealio/errors/504.html', status=504)

def custom_403(request, exception):
    return render(request, 'edudealio/errors/403.html', status=403)

def custom_401(request):
    return render(request, 'edudealio/errors/401.html', status=401)

def custom_502(request):
    return render(request, 'edudealio/errors/502.html', status=502)

def custom_503(request):
    return render(request, 'edudealio/errors/503.html', status=503)

def custom_400(request, exception):
    return render(request, 'edudealio/errors/400.html', status=400)