from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctorLogin = models.CharField(max_length=50, null=True, blank=True)
    doctorMail = models.CharField(max_length=50, null=True, blank=True)
    doctor = models.CharField(max_length=50, choices=[
        ('is_radiologist', 'Рентгенолог'),
        ('is_gynecologist', 'Гинеколог'),
        ('is_ophthalmologist', 'Офтальмолог'),
        ('is_cardiologist', 'Кардиолог'),
        ('is_procedural_nurse', 'Процедурная медицинская сестра (анализы)'),
        ('is_mammologist', 'Маммолог'),
        ('is_urologist', 'Уролог'),
        ('is_therapist', 'Терапевт'),
    ])
    

    def __str__(self):
        return f'{self.user.username} Profile'

class Patient(models.Model):
    
    patientPassportDetails = models.CharField(max_length=50, null=True, blank=True)
    patientName = models.CharField(max_length=50, null=True, blank=True)
    patientPhone = models.CharField(max_length=50, null=True, blank=True)
    patientAge = models.CharField(max_length=50, null=True, blank=True)
    patientGender = models.CharField(max_length=50, null=True, blank=True)
    

    def __str__(self):
        return f'{self.patientName}'
    
class Patient_Record(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Profile, through='Patient_Record_Doctor')

    def __str__(self):
        return f'Record for {self.patient}'
    

class Patient_Record_Doctor(models.Model):
    patient_record = models.ForeignKey(Patient_Record, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pathology = models.CharField(max_length=255, default='')
    briefDoctorReport = models.CharField(max_length=255, default='')
    doctorReportWord = models.FileField(upload_to='word_documents/', default='')

    def __str__(self):
        return f'{self.patient_record} by {self.doctor}'




