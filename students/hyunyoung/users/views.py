import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            email    = data['email']
            password = data['password']

            email_form    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            password_form = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(email_form, email):
                return JsonResponse({'message':'EMAIL FORM ERROR'}, status=400)

            if not re.match(password_form, data['password']):
                return JsonResponse({'message':'PASSWORD FORM ERROR'}, status=400)
            
            if User.objects.filter(email=email):
                return JsonResponse({'message':'ALREADY EXIST'}, status=400)
        
            User.objects.create(
                name         = data['name'],
                email        = email,
                password     = password,
                phone_number = data['phone'],
            )

            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)