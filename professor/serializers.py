from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from professor.models import Professor

class ProfessorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Professor.objects.all(),
                message="A user with that username already exists."
            )
        ]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Professor.objects.all())]
    )
    cpf = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Professor.objects.all(),
                message="A user with that cpf already exists."
            )
        ]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Professor
        fields = ['id', 'first_name', 'last_name', 'is_superuser', 'email', 'username', 'cpf', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_cpf(self, value):
        if len(value) != 11 or not value.isdigit():
            raise serializers.ValidationError("CPF must contain exactly 11 numeric digits.")
        return value

    def create(self, validated_data: dict) -> Professor:
        user = Professor(
            username=validated_data['username'],
            email=validated_data['email'],
            cpf=validated_data['cpf'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance: Professor, validated_data: dict) -> Professor:
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.cpf = validated_data.get('cpf', instance.cpf)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
