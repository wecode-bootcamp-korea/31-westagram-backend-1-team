import json , re
from django.http import JsonResponse
from django.views import View
from .models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email_check     = re.compile('/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$/')
            password_check  = re.compile('/^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/')
            
            if data["email"] in User.objects.filter(email=data['email']):
                return JsonResponse({"massage":"This email has already been registered."}, status=401)
            else:
                if email_check.match(data["email"]) == False: 
                    return JsonResponse({"massage":"Invalid e-mail format."}, status=401)
                elif password_check.match(data["password"]) == False:
                    return JsonResponse({"massage":"Invalid password format."}, status=401)
                else:
                    User.objects.create(
                        name            =  data["name"],
                        email           =  data['email'],
                        password        =  data['password'],
                        phone           =  data['phone'],
                        date_of_birth   =  data['date_of_birth']
                    )
                return JsonResponse({'message':'sign up completed.'}, status=201)
        except KeyError:
            return JsonResponse({'key_error'}, status=401)