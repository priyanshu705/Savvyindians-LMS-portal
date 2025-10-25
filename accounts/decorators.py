from functools import wraps

from django.shortcuts import redirect


def admin_required(
    function=None,
    redirect_to="/",
):
    """
    Decorator for views that checks that the logged-in user is a superuser,
    redirects to the specified URL if necessary.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_active and request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_to)

        return wrapper

    if function:
        return decorator(function)
    return decorator


def lecturer_required(
    function=None,
    redirect_to="/",
):
    """
    Decorator for views that checks that the logged-in user is a lecturer,
    redirects to the specified URL if necessary.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_active and (
                request.user.is_lecturer or request.user.is_superuser
            ):
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_to)

        return wrapper

    if function:
        return decorator(function)
    return decorator


def student_required(
    function=None,
    redirect_to="/accounts/student/login/",
):
    """
    Decorator for views that checks that the logged-in user is a student,
    redirects to the login page if necessary.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_active and (
                request.user.is_student or request.user.is_superuser
            ):
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_to)

        return wrapper

    if function:
        return decorator(function)
    return decorator
