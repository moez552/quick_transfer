from rest_framework import serializers
from .models import History,Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('transaction_type', 'amount','created_date','status','receiver')
    def create(self, validated_data):
        try:
            user =  self.context['request'].user
            profile = Profile.objects.get(user=user)
            print(validated_data)
            history = History.objects.create(
                profile = profile,
                amount=validated_data['amount'],
                transaction_type = validated_data['transaction_type'],
                receiver = validated_data['receiver']
            ) 
            history.save()
            return history
        except ValidationError as e:
            raise serializers.ValidationError({"message":e.message,"code":e.code})

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username')
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Profile
        fields = ('balance', 'max_withdraw','user','verified')

            
class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password','email','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
                validated_data['username'],email=validated_data['email'],first_name=validated_data['first_name'],last_name=validated_data['last_name']
        )
        user.set_password(password)
        user.save()
        return user
