from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AllowAuthUserOnly(MiddlewareMixin):
    def process_request(self, request):
        if not request.path.startswith('/users/'):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('auth:login'))
            # Continue processing the request as usual:
        return None
