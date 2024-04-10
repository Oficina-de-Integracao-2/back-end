from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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

    class Meta:
        model = Professor
        fields = ['id', 'first_name', 'last_name', 'is_superuser', 'email', 'username', 'cpf']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data: dict) -> Professor:
        return Professor.objects.create_superuser(**validated_data)

    def update(self, instance: Professor, validated_data: dict) -> Professor:
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
