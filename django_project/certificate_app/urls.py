from django.urls import path
from . import views

app_name = 'certificate_app'  # This is the namespace for your app's URL patterns

urlpatterns = [
    # Define URL patterns and map them to view functions
    path('', views.HomeView.as_view(), name='home'),  # Homepage
    path('create_certificate/',
         views.CreateCertificateView.as_view(),
         name='create_certificate'),  # Certificate creation page
    path('verify_certificate/',
         views.VerifyCertificateView.as_view(),
         name='verify_certificate'),  # Certificate verification page
    path('verify/<str:token>/',
         views.VerifyJWTView.as_view(),
         name='verify_jwt'),  # Verify JWT (JSON Web Token)
]
