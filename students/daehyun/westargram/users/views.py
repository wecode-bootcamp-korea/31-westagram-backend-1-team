import json, re

from django.http import JsonResponse
from django.views import View

from users.models import User


class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            
            EMAIL_RULE    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PASSWORD_RULE = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'EMAIL_ALREADY_EXISTS'}, status = 400)
            
            if not re.match(EMAIL_RULE, email):
                return JsonResponse ({'message' : 'INVALID_EMAIL'}, status = 400)
            
            if not re.match(PASSWORD_RULE, password):
                return JsonResponse ({'message' : 'INVALID_PASSWORD'}, status = 400)
            
            User.objects.create(
                name         = data['name'],
                email        = email,
                password     = password,
                phone_number = data['phone_number']
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
                
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        
class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            
            EMAIL_RULE    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            PASSWORD_RULE = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            if not re.match(EMAIL_RULE, email):
                return JsonResponse ({'message' : 'INVALID_USER_EMAIL'}, status = 400)
            
            if not re.match(PASSWORD_RULE, password):
                return JsonResponse ({'message' : 'INVALID_USER_PASSWORD'}, status = 400)
            
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'EMAIL_NOT_EXISTS'}, status = 400)
            
            if User.objects.get(email=email).password != password:
                return JsonResponse({'message' : 'PASSWORD_INCORRECT'}, status = 400)
            
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
                
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)