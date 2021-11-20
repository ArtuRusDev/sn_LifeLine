from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AllowStaffUserOnly(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_staff:
                return HttpResponseRedirect(reverse('news:main'))
            # Continue processing the request as usual:
        return None
