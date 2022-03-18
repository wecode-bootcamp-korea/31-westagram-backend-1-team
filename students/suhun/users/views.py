import json , re
from django.http import JsonResponse
from django.views import View
from models import User

class SignUP(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email_check     = re.compile('/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$/')
            password_check  = re.compile('/^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/')
            if data["email"] in User.objects.filter(email=data['email']):
                return JsonResponse({"이미 가입된 이메일 입니다."}, status=401)
            else:
                if email_check.match(data["email"]) == False:  #벨리데이션이랑 비교 잘못된 형식:
                    return JsonResponse({"틀린 이메일 형식입니다."}, status=401)
                elif password_check.match(data["password"]) == False:
                    return JsonResponse({"틀린 비밀번호 형식입니다."}, status=401)
                else:
                    User.objects.create(
                        name            =  data["name"],
                        email           =  data['email'],
                        password        =  data['password'],
                        phone           =  data['phone'],
                        date_of_birth   =  data['data_of_birth']
                    )
            return JsonResponse({'message':'회원가입이 완료되었습니다.'}, status=201)
        except KeyError:
            return JsonResponse({'key_error'}, status=401)
    
#1.  바디에서 정보를 받아온다. 
# (이름, 이메일, 비밀번호, 휴대전화, 생일, 가입일자, 업데이트 일자)
#2. 이메일이 형식에 맞는지 확인
#3. 이메일이 저장소에서 유일한지 (중복 검사)
#4. 형식이 맞고 중복이 없다면 받은 모든 바디의 내용으로 objects.create