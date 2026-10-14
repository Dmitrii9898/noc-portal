from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def staff_required(view):
    @login_required
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_admin_role or user.is_staff_role:
            return view(request, *args, **kwargs)
        raise PermissionDenied("Раздел доступен сотрудникам центра.")
    return wrapper


def admin_required(view):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_admin_role:
            return view(request, *args, **kwargs)
        raise PermissionDenied("Раздел доступен только администратору.")
    return wrapper
