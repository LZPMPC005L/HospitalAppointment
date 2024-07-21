from rest_framework import serializers
from .models import MedicalRecords, Prescription, Medicine, Customer, Doctor, Appointment, MedicalOrder

# serializers
class MedicalRecordSerializer(serializers.ModelSerializer):
    #add a custom field to show formatted time
    formatted_time = serializers.SerializerMethodField()

    def get_formatted_time(self, obj):
        # format the time field to show only date and hour
        return obj.time.strftime('%d-%m-%Y %H:%M') if obj.time else None

    class Meta:
        model = MedicalRecords
        fields = ['id', 'doctor_id', 'patient_id', 'formatted_time', 'prescriptionRecord']

#Medicine
class MedicineSerializer(serializers.ModelSerializer):
    last_modified = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'total_stock', 'last_modified']

#Prescription
class PrescriptionSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    medicine_details = MedicineSerializer(source='medicine', read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'medicine','medicine_details','dosage', 'medication_instructions', 'prescription_time']
        depth = 1


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'address', 'is_insurance', 'balance','claim_rate']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'department']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time', 'is_confirmed']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalOrder
        fields = ['id', 'appointment_id', 'medical_expense', 'is_claim', 'is_pay', 'create_time']