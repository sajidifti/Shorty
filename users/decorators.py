from django.shortcuts import redirect

def unauthenticated_users_only(function=None, redirect_url="home"):
    """
    Allows access to only unauthenticated users
    """

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper_func
    if function is None:
        return decorator
    else:
        return decorator(function)