from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, TestUserSerializer, UserListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def user_api_view(request):
    if request.method == 'GET':
        # queryset
        users = User.objects.all().values('id', 'username', 'email', 'password')
        # users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        '''
            test_data = {
                'name': 'develop',
                'email': 'test@gmail.com'
            }
            test_user = TestUserSerializer(data=test_data, context=test_data)
            if test_user.is_valid():
                test_user.save()
                # print(test_user.validated_data)
            else:
                print(test_user.errors)
        '''
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_view(request, pk=None):
    # Consulta
    user = User.objects.filter(id=pk).first()
    # Validacion
    if user:
        # Obtener
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':  # Actualizar
            user_serializer = TestUserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':  # Eliminar
            user.delete()
            return Response({'message': 'Usuario eliminado correctamente'}, status=200)
    return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
