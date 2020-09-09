from django.http.response import HttpResponse
from django.views.generic.base import View

# Create your views here.


#
class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the polls index.")
