from django.http.response import JsonResponse
from django.views import View
from rest_framework.decorators import api_view

# Create your views here.
class UserView(View):
    
    @api_view(['POST'])
    def test(request):
        if request.method == 'POST':
            res:dict={}
            res["message"] = "This is a test API"
            res["status"] = True
            return JsonResponse(res)
