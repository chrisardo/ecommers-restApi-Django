from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from users.serializers import UserSerializer
from users.serializers import UserTokenSerializer
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta
# Create your views here.
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
