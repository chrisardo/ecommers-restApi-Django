from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from users.serializers import UserTokenSerializer
from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework.views import APIView 
from users.authentication_missing import Authentication

# Create your views here.
class UserToken(Authentication, APIView):
    '''
    validar token
    '''
    def get(self, request, *args, **kwargs):
        #username = request.GET.get('username')
        try:
            user_token,_ = Token.objects.get_or_create(user = self.user)
            user = UserTokenSerializer(self.user)
            return Response({
                'token': user_token.key,
                'user': user.data
                }, status= status.HTTP_200_OK)
        except:
            return Response({'error': 'No se ha encontrado un usuario con estas credenciales.'}, status= status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data= request.data, context= {'request': request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user= user)
                user_serializer = UserTokenSerializer(user)
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso.',
                    }, status= status.HTTP_201_CREATED)
                else:
                    ''' Se comprueba si el token no ha expirado '''
                    '''
                    all_sessions = Session.objects.filter(expire_date__gte= datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete() # Borramos el token anterior
                    token = Token.objects.create(user= user) # Se crea un nuevo token
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso.',
                    }, status= status.HTTP_201_CREATED)
                    '''
                    token.delete()
                    return Response({'error': 'Este usuario ya ha iniciado sesion.'}, status= status.HTTP_409_CONFLICT)
                

            else:
                return Response({'error': 'Este usuario no puede iniciar sesion.'}, status= status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrectos.'}, status= status.HTTP_400_BAD_REQUEST)

class Logaut(APIView):
    def get(self, request, *args, **kwarg):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key = token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()
                session_message = 'Sesiones de usuario eliminados.'
                token_message = 'Token eliminado'
                return Response({'token_message': token_message, 'session_message': session_message}, status= status.HTTP_200_OK)
            return Response({'error': 'No se ha encontrado un usuario con estas credenciales.'}, status=status.HTTP_400_BAD_REQUEST)
        except:    
            return Response({'error': 'No se ha encontrado token en la peticion.'}, status=status.HTTP_409_CONFLICT)
