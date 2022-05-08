from numpy import source
from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User, Patient, Doctor

class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='patient.uploadimage.image')
    class Meta:
        model=User
        fields=['username', 'email', 'is_patient', 'phone', 'age', 'image']


class PatientSignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username', 'email', 'password', 'password2', 'phone', 'age']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            age=self.validated_data['age']     
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_patient=True
        user.save()
        Patient.objects.create(user=user)
        return user     

class DoctorSignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={"input_type":"password"}, write_only=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username', 'email', 'password', 'password2', 'phone', 'age']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            age=self.validated_data['age']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_doctor=True
        user.save()
        Doctor.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: This credentials does not meet any of our records, please make sure you have entered the right credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
    
    
#from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)