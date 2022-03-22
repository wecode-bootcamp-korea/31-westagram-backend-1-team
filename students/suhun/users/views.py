import json , re , bcrypt

from django.http import JsonResponse
from django.views import View

from .models import User

class SignUpView(View):
    def post(self, request):
        try: 
            data = json.loads(request.body)
            name            = data['name']
            email           = data['email']
            password        = data['password']
            phone           = data['phone']
            date_of_birth   = data['date_of_birth']
            
            PASSWORD_CHECK  = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
            EMAIL_CHECK     = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
            if User.objects.filter(email = email).exists():
                return JsonResponse({"massage":"already registered."}, status=401)
            
            if not re.match(EMAIL_CHECK, email): 
                return JsonResponse({"massage":"Invalid e-mail format."}, status=401)
            
            if not re.match(PASSWORD_CHECK, password):
                return JsonResponse({"massage":"Invalid password format."}, status=401) 
            
            new_salt = bcrypt.gensalt()
            encoded_password     = password.encode('utf-8')
            hashed_password      = bcrypt.hashpw(encoded_password , new_salt)
            decode_hash_password = hashed_password.decode('utf-8')
            User.objects.create(
                        name            =  name,
                        email           =  email,
                        password        =  decode_hash_password,
                        phone           =  phone,
                        date_of_birth   =  date_of_birth
                    )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEYERROR'}, status=401)


class SignInView(View):    
    def post(self,request):
        try:
            data = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
            
            if not User.objects.filter(email = email, password = password): 
                return JsonResponse({"message": "INVALID_USER"}, status= 401)
            return JsonResponse({"message": "SUCCESS"}, status = 200)   
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)