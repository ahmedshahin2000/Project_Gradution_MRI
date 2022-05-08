from django.urls import path, include
from .views import (PatientSignupView, DoctorSignupView, 
                    CustomAuthToken, LogoutView, ChangePasswordView,
                    PatientOnlyView, DoctorOnlyView) 

urlpatterns = [
    path('signup/patient/', PatientSignupView.as_view()),
    path('signup/doctor/', DoctorSignupView.as_view()),
    path('login/', CustomAuthToken.as_view(), name='auth_token'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('patient/dashboard/', PatientOnlyView.as_view(), name='patient-dashboard'),
    path('doctor/dashboard/', DoctorOnlyView.as_view(), name='doctor-dashboard'),
]