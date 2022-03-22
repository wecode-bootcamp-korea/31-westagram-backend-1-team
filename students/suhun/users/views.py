import json , re , bcrypt , jwt

from django.http import JsonResponse
from django.views import View

from django.conf import settings

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
                return JsonResponse({"massage":"REGISTERED."}, status=401)
            
            if not re.match(EMAIL_CHECK, email): 
                return JsonResponse({"massage":"INVALID_EMAIL."}, status=401)
            
            if not re.match(PASSWORD_CHECK, password):
                return JsonResponse({"massage":"INVALID_PASSWORD."}, status=401) 
            
            hashed_password      = bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')
            User.objects.create(
                        name            =  name,
                        email           =  email,
                        password        =  hashed_password,
                        phone           =  phone,
                        date_of_birth   =  date_of_birth
                    )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)


class SigninView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
            email          = data["email"]
            input_password = data["password"]
            user_id = User.objects.get(email= email).id
            
            checkpw_input_db = bcrypt.checkpw(input_password.encode('utf-8'), User.objects.get(email= email).password.encode('utf-8') )

            if not User.objects.filter(email=email).exists() :
                return JsonResponse( {'meassage' : 'INVALID EMAIL.'}, status = 401)        
            if not checkpw_input_db:
                return JsonResponse( {'message' : 'INVALID PASSWORD.' } , status = 401)
            new_token        = jwt.encode( {"user": user_id } , settings.SECRET_KEY , algorithm= settings.ALGORITHM)
            return JsonResponse({"token": new_token }, status = 200)
 
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=401)
