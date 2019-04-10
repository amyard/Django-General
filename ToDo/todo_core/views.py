from django.shortcuts import render


def home(request):
    return render(request, 'todo_core/main.html', {'info': 'It\'s working.'})