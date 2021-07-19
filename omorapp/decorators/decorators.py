from django.urls import reverse
from django.shortcuts import redirect


def un_authenticated_users(view_func):
    def wrapper_func(request, *arg, **kwargs):
        if request.user.is_authenticated:
            return redirect('omorapp:home')
        return view_func(request, *arg, **kwargs)
    return wrapper_func
