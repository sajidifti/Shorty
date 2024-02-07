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


def authenticated_users_only(function=None, redirect_url="home"):
    """
    Allows access to only authenticated users
    """

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper_func
    if function is None:
        return decorator
    else:
        return decorator(function)


def admin_only(view_func):
    """
    Allows Admin Only
    """
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == "generaluser":
                return redirect("home")

            if group == "admin":
                return view_func(request, *args, **kwargs)

    return wrapper_function
