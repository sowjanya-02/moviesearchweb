from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .es_connect import es

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)
    
    def validate(self, data):
        # Perform uniqueness validation for email and username against Elasticsearch
        email = data.get('email')
        username = data.get('username')
        es.index('users',body={'username':'testdev'})
        # Check uniqueness against Elasticsearch data
        if email and username:

            email_exists = es.search(index='users', body={'query': {'term': {'email.keyword': email}}})
            if email_exists['hits']['total']['value'] > 0:
                raise serializers.ValidationError('This email is already in use.')

            username_exists = es.search(index='users', body={'query': {'term': {'username.keyword': username}}})
            if username_exists['hits']['total']['value'] > 0:
                raise serializers.ValidationError('This username is already in use.')

        return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')