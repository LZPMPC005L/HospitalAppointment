from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime
from django.core.exceptions import ValidationError
class Customer(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200)

    is_insurance = models.BooleanField(default=False)
    balance = models.FloatField(default=0.0)
    claim_rate = models.FloatField(default=0.0)

    groups = models.ManyToManyField(Group, related_name='customer_group')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'customer'

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'doctor'

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.name} - {self.date}"

    class Meta:
        db_table = 'appointment'


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    total_stock = models.PositiveIntegerField(default=100)
    last_modified = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.name

    def decrease_stock(self, dosage):
        if dosage > self.total_stock:
            raise ValueError('Dosage exceeds available stock.')
        self.total_stock -= dosage
        self.save()

    class Meta:
        db_table = 'medicine'


class Prescription(models.Model):
    patient = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication_instructions = models.TextField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.PositiveIntegerField()

    prescription_time = models.TimeField(default=datetime.now)

    def clean(self):
        if self.dosage > self.medicine.total_stock:
            raise ValidationError('Dosage exceeds available stock.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.medicine.decrease_stock(self.dosage)

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.name} - {self.medicine.name}"

    class Meta:
        db_table = 'prescription'



# Define medical records
class MedicalRecords(models.Model):
    id = models.AutoField(primary_key=True)
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    #doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    #patient = models.ForeignKey(Customer, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now())
    #time = models.DateTimeField(default=datetime.now)
    prescriptionRecord = models.CharField(max_length=1000)

    def __str__(self):
        return self.id + self.prescriptionRecord

    class Meta:
        db_table = 'medicalRecords'

class MedicalOrder(models.Model):
    id = models.AutoField(primary_key=True)
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medical_expense = models.FloatField()
    is_claim = models.BooleanField(default=False)
    is_pay = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return str(self.id) + str(self.medical_expense)

    class Meta:
        db_table = 'medical_order'