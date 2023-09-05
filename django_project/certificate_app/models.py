from django.db import models

# Certificate model to store certificate information
class Certificate(models.Model):
    name = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    date = models.DateField()
    email = models.EmailField(max_length=254, blank=True)
    verification_code = models.CharField(max_length=20, unique=True)

# CertificateVerification model to store verification details
class CertificateVerification(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=100)
