from django.shortcuts import render
from django.views import View
from .models import Certificate, CertificateVerification
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from datetime import datetime, timedelta
from reportlab.lib.colors import HexColor
import string
import secrets
import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY')


# function for generating verification code
def generate_verification_code(length=10):
    characters = string.ascii_letters + string.digits
    verification_code = ''.join(
        secrets.choice(characters) for _ in range(length))
    return verification_code


# Home page view
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})


# View for creation of certificate
class CreateCertificateView(View):
    def get(self, request):
        return render(request, 'create_certificate.html', {})

    def post(self, request):
        # Retrieve form data
        name = request.POST.get('name')
        signature = request.POST.get('signature')
        course = request.POST.get('course')
        date = request.POST.get('date')
        subtitle = request.POST.get('subtitle')
        email = request.POST.get('email')
        verification_code = generate_verification_code()
        print("eemai=", email)
        # Create a Certificate object
        certificate = Certificate.objects.create(
            name=name,
            signature=signature,
            date=date,
            subtitle=subtitle,
            verification_code=verification_code,
            email=email,
            course=course)

        # Create a CertificateVerification object
        certificate_verification = CertificateVerification.objects.create(
            certificate=certificate, verification_code=verification_code)

        # Prepare the PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="certificate.pdf"'

        # Create a canvas to draw on the PDF
        c = canvas.Canvas(response, pagesize=(700, 500))

        c.setFont("Helvetica-Bold", 30)  # Certificate title
        c.setFillColor(HexColor("#007bff"))
        c.drawString(150, 400, "Certificate of Completion")

        c.setFillColor(HexColor("#000000"))
        c.setFont("Helvetica", 20)  # Certificate description
        c.drawString(100, 320, "This is to certify that")

        c.setFont("Helvetica-Bold", 24)  # Certificate Name
        c.drawString(200, 280, name)

        c.setFont("Helvetica", 20)  # Certificate Subtitle
        c.drawString(200, 255, subtitle)

        c.setFont("Helvetica", 20)  # Certificate Course
        c.drawString(200, 230, "Course: " + course)

        c.setStrokeColor(HexColor("#007bff"))  # Decorative line
        c.line(100, 180, 600, 180)

        c.setFont("Helvetica", 20)  # Date and signature
        c.drawString(
            100, 150,
            "Date: " + date + "                  Signature: " + signature)

        c.setFillColor(HexColor("#777777"))
        c.setFont("Helvetica", 12)  # Certificate code
        c.drawString(90, 40, "Certificate Code: " + verification_code)

        c.setStrokeColor(HexColor("#0000FF"))  # Decorative border
        c.rect(50, 25, 600, 450, stroke=1, fill=0)

        # Save the PDF content
        c.save()
        return response


#View for verifying certificate
class VerifyCertificateView(View):
    def get(self, request):
        # view logic for verifying certificates
        return render(request, 'verify_certificate.html', {})

    def post(self, request):
        # Retrieve verification code from form data
        verification_code = request.POST.get('vcode')

        try:
            # Retrieve the certificate associated with the verification code
            certificate_verification = CertificateVerification.objects.get(
                verification_code=verification_code)

            # Get the certificate object
            certificate = certificate_verification.certificate
            recipient_email = certificate.email

            # Generate JWT token
            payload = {
                'verification_code': verification_code,
                'exp':
                datetime.utcnow() + timedelta(days=1)  # Token expiration time
            }
            # Generate JWT token for certificate verification link
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            if recipient_email:
                subject = 'Certificate Verification'
                message = f'Click the following link to verify your certificate: https://sahayak.punampanchal.repl.co/verify/{token}'
                recipient_list = [recipient_email]
                from_email = 'panchalpunam143@gmail.com'
                send_mail(subject, message, from_email, recipient_list)
                message_result = True
            else:
                message_result = False

            context = {
                'certificate': certificate,
                'message_sent': message_result
            }
            return render(request, 'verification_result.html', context)
        except CertificateVerification.DoesNotExist:
            error_message = 'This is not a valid Certificate Code'
            return render(request, 'verify_certificate.html',
                          {'error_message': error_message})


# View for verifying jwt token
class VerifyJWTView(View):
    def get(self, request, token):
        try:
            # Decode and verify JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            verification_code = payload.get('verification_code')
            try:
                certificate_verification = CertificateVerification.objects.get(
                    verification_code=verification_code)
                certificate = certificate_verification.certificate
                context = {
                    'certificate': certificate,
                    'verification_status': 'This is Verified Certificate'
                }
            except CertificateVerification.DoesNotExist:
                context = {'verification_status': 'Certificate not found'}
        except jwt.ExpiredSignatureError:
            context = {'verification_status': 'The token is expired'}
        except jwt.DecodeError:
            context = {'verification_status': 'Token is invalid'}

        return render(request, 'verification_result.html', context)
