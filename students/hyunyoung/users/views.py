import bcrypt, json, jwt, re

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone']

            email_form    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            password_form = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            
            if not re.match(email_form, email):
                return JsonResponse({'message':'EMAIL FORM ERROR'}, status=400)

            if not re.match(password_form, data['password']):
                return JsonResponse({'message':'PASSWORD FORM ERROR'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'ALREADY EXIST'}, status=400)
        
            User.objects.create(
                name         = name,
                email        = email,
                password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                phone_number = phone_number,
            )

            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse( {'message': 'INVALID_USER'}, status=401)

            token = jwt.encode({'user_id':user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'token': token}, status=200)

        except User.DoesNotExist:
            return JsonResponse( {'message': 'YOUR EMAIL DOES NOT EXIST'}, status=400)

        except KeyError:
            return JsonResponse( {'message': 'KEY_ERROR'}, status=400)