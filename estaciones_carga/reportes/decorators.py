from django.http import HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser) or not hasattr(request.user.profile, 'user_type') or request.user.profile.user_type != 'admin':
            return HttpResponseForbidden("No tienes acceso a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
