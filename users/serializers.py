from rest_framework import serializers
from .models import User

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Encriptar password
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email']
        }


class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()

    def validate_name(self, value):
        if 'developer' in value:  # Validacion personalizada
            raise serializers.ValidationError(
                'Error: El nombre no puede contener la palabra develop')
        return value

    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError(
                'Error: El email no puede estar vacio')
        return value

    def validate(self, data):
        if data['name'] in data['email']:
            raise serializers.ValidationError(
                'Error: El email no puede contener el nombre')
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    '''
    def save(self):
        print(self.validated_data)
        user = User.objects.create(**self.validated_data)
        return user
    '''
