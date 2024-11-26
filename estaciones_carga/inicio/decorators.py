from django.http import HttpResponseForbidden

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.user_type != 'admin':
            return HttpResponseForbidden("No tienes acceso a esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

