from rest_framework import serializers
from .models import History,Profile
from django.core.exceptions import ValidationError
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('transaction_type', 'amount','created_date','status','receiver')
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.transaction_type != 'TR':
            ret.pop('receiver')
        return ret
    def create(self, validated_data):
        try:
            user =  self.context['request'].user
            profile = Profile.objects.get(id=user.id)
            print(validated_data)
            if validated_data['transaction_type'] != 'TR':
            
                history = History.objects.create(
                    profile = profile,
                    amount=validated_data['amount'],
                    transaction_type = validated_data['transaction_type'],
                )
            else:
                if not validated_data['receiver']:
                    raise serializers.ValidationError({"message":'catched receiver',"code":5})
                history = History.objects.create(
                profile = profile,
                amount=validated_data['amount'],
                transaction_type = validated_data['transaction_type'],receiver = validated_data['receiver']
            )
            history.save()
            return history
        except ValidationError as e:
            raise serializers.ValidationError({"message":e.message,"code":e.code})

    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('balance', 'max_withdraw','email','username','first_name','last_name','verified','profile_type','business_name')
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.profile_type == 'PL':
            ret.pop('business_name')
        return ret
class OuterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username','first_name','last_name','profile_type','business_name')
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.profile_type == 'PL':
            ret.pop('business_name')
        return ret

            
class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'password','email','first_name','last_name','profile_type','business_name')
        extra_kwargs = {'password': {'write_only': True}}
        

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            user = Profile.objects.create_user(
                    username=validated_data['username'],email=validated_data['email'],password=password,
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],profile_type=validated_data['profile_type'],business_name=validated_data['business_name']
            )
            user.save()
            return user
        except ValidationError as e:
            raise serializers.ValidationError({'message':e.message})
