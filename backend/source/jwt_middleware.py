
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from accounts.utils import resend_otp_func
from rest_framework_simplejwt.tokens import AccessToken    
import ast
from django.http import QueryDict
from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomAuthBackend(BaseBackend):
    def authenticate(self,isGoogleAuth=False, username=None, password=None):
        # Implement your custom authentication logic here
        # For example, check if a one-time token sent via email is valid
        user = User.objects.just_get_user_by_username(username)
        if not user: 
            user = User.objects.get_user_by_email(username)

        if not user:
            raise ValueError({"message":"Invalid credentials. Please try again.","code":"400"})
            
        
        if not isGoogleAuth:
            if not password:
                raise ValueError({"message":"Password Required.","code":"400"})
            
            if not user.check_password(password):
                raise ValueError({"message":"Incorrect password. Please try with right credentials.", "email": username,"code":"404"})
        
        if not user.is_active:
            resend_otp_func(subject="Account Verification OTP - PlayApp",email=user.email,purpose="verify_account")
            raise Exception({"message":"INACTIVE. This user exists but it's not verified yet. We have sent OTP on linked email of this account. Please Verify.","email":user.email,"code":"505"}) 

        access_token = AccessToken.for_user(user)
        access_token['id'] = user.id
        access_token["username"] = user.username
        access_token["is_admin"] = user.is_admin
        User.objects.custom_save(user)
        return ({
            'access': str(access_token),
            'refresh': str(access_token)
        })
        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):

        data = QueryDict('', mutable=True)
        data.update(request.data)
        data = data.dict()
        username = data.get("username", None)
        password = data.get("password", None)

        if not username :
            return Response({"message":"Username required."},status=400)

        if not password :
            return Response({"message":"Username required."},status=400)
        
        username = username.lower().strip()
        print(username,password)
        try:
            data = CustomAuthBackend().authenticate(isGoogleAuth=False,username=username,password=password)
            return Response(data, status=200)
        except Exception as e:
            print(e)
            try:
                error_dict = ast.literal_eval(str(e))
                # print(error_dict.get('code',401))
                return Response(error_dict, status=error_dict.get('code',401))
            except Exception:
                return Response({"message":"Unexcepted Error."}, status=400)