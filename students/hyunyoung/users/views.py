import re
import json

from django.http  import JsonResponse
from django.views import View
from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            email_form    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            password_form = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")


            if not email_form.match(data['email']):
                return JsonResponse({'message':'EMAIL FORM ERROR'}, status=400)
            if not password_form.match(data['password']):
                return JsonResponse({'message':'PASSWORD FORM ERROR'}, status=400)
          
            users = User.objects.filter(email=data['email'])
            if users:
                return JsonResponse({'message':'this email already exists'}, status=400)
                

            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone'],
            )

            return JsonResponse({'message':'SUCCESS'}, status=201)

        except:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)