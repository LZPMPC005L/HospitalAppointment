import json
from django.core.serializers import serialize
from django.db.migrations import serializer
from .models import Customer, Doctor, Appointment, MedicalRecords, Prescription, Medicine, MedicalOrder
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from .serializers import MedicalRecordSerializer, PrescriptionSerializer, MedicineSerializer, CustomerSerializer, DoctorSerializer, AppointmentSerializer, OrderSerializer


# Define harmonised return formats
def resposeBody(code, meassge, data):
    return {
        'code': code,
        'message': meassge,
        'data': data
    }

# Update the medical record
# need to pass in prescriptionRecord patient_id doctor_id
@csrf_exempt
def update_medical_record(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MedicalRecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(resposeBody(200, 'created successfully', None))
        return JsonResponse({'status': 'error', 'message': serializer.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Query medical records
# Query all medical records without passing in patient_id.
# If patient_id is passed in, query the corresponding patient's medical record.
def get_medical_record(request, patient_id=None):
    if patient_id is None:
        # If patient_id is not provided, all medical records are returned
        # medical_records = MedicalRecords.objects.all()
        medical_records = MedicalRecords.objects.all()
        serializer = MedicalRecordSerializer(medical_records, many=True)
        # Execute your logic here, e.g. serialise all medical records and return JSON responses
        return JsonResponse(resposeBody(200, 'successes', serializer.data))
    else:
            record = MedicalRecords.objects.filter(patient_id=patient_id)
            serializer = MedicalRecordSerializer(record, many=True)
            # Execute your logic here, such as serialising medical records and returning JSON responses
            return JsonResponse(resposeBody(200, 'successes', serializer.data))


@csrf_exempt
def register_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            address = data.get('address')
            is_insurance = data.get('is_insurance', False)
            balance = data.get('balance', 0.0)
            claim_rate = data.get('claim_rate', 0.00)

            customer = Customer.objects.create_user(username = email, email = email, address = address, name = name, is_insurance = is_insurance, balance = balance, claim_rate = claim_rate)

            return JsonResponse({'message' : 'Patient registered successfully', 'customer_id' : customer.pk, 'name': customer.name, 'email': customer.email, 'address': customer.address,'is_insurance': customer.is_insurance, 'balance': customer.balance, 'claim_rate': customer.claim_rate})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        customers = Customer.objects.all()
        customer_data = []
        for customer in customers:
            customer_data.append({
                'id': customer.pk,
                'name': customer.name,
                'email': customer.email,
                'address': customer.address,
                'is_insurance': customer.is_insurance,
                'balance': customer.balance,
                'claim_rate': customer.claim_rate
            })
        return JsonResponse({'error' : 'Invalid Request Method'}, status = 400)


@csrf_exempt
def add_doctor(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Doctor added successfully'}, status = 201)
        return JsonResponse({'error':'Invalid request method'}, status = 400)
@csrf_exempt
def doctor_list(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        doctor_data = []

        for doctor in doctors:
            doctor_data.append({
                'name' : doctor.name,
                'department' : doctor.department
            })

        return JsonResponse({'doctors' : doctor_data})
    else:
        return JsonResponse({'error':'Invalid Request Method'}, status = 400)


@csrf_exempt
def appointment_list(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all()
        appointments_data = []
        for appointment in appointments:
            appointment_data = {
                'id':appointment.id,
                'patient':{
                    'id':appointment.patient.id,
                    'name':appointment.patient.name,
                    'email':appointment.patient.email,
                    'address':appointment.patient.address,
                    'is_insurance':appointment.patient.is_insurance,
                    'balance':appointment.patient.balance,
                    'claim_rate':appointment.patient.claim_rate,
                },
                'doctor':{
                    'id':appointment.doctor.id,
                    'name':appointment.doctor.name,
                    'department':appointment.doctor.department,
                },
                'date':appointment.date.strftime('%d-%m-%Y'),
                'time':appointment.time.strftime('%H:%M'),
                'is_confirmed':appointment.is_confirmed,
            }
            appointments_data.append(appointment_data)
        return JsonResponse({'appointments': appointments_data})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            date_str = data.get('date')
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_str = data.get('time')#get appoinement time
            time = datetime.strptime(time_str, '%H:%M').time()
            doctor_id = serializer.validated_data.get('doctor')

            conflicting_appointments = Appointment.objects.filter(doctor_id=doctor_id, date=date, time=time)
            if conflicting_appointments.exists():
                return JsonResponse({'error': 'Appointment time conflicts with existing appointment'}, status=400)
            else:
                serializer.save(date=date, time=time)
                return JsonResponse({'message': 'Appointment created successfully','appointment':serializer.data})
        else:
            return JsonResponse({'error':serializer.errors}, status = 400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status = 405)

#add medicine
@csrf_exempt
def add_medicine(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        name = data.get('name')
        total_stock = data.get('total_stock')
        last_modified = data.get('last_modified') #manually

        try:
            existing_medicine = Medicine.objects.get(name=name)
            existing_medicine.total_stock += int(total_stock)
            existing_medicine.last_modified = last_modified
            existing_medicine.save()

            serializer = MedicineSerializer(existing_medicine)
            return JsonResponse({'message': 'Medicine has already in it, added successfully', 'medicine': serializer.data}, status = 200)

        except Medicine.DoesNotExist:
            new_medicine = Medicine.objects.create(name=name, total_stock=total_stock, last_modified=last_modified)
            serializer = MedicineSerializer(new_medicine)
            return JsonResponse({'message': 'Medicine added successfully','medicine':serializer.data}, status = 201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status = 400)

#show medicines
@csrf_exempt
def show_medicines(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return JsonResponse({'medicines' : serializer.data})

#add prescription
@csrf_exempt
def add_prescription(request, patient_id):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        patient = Customer.objects.get(pk=patient_id) #get patient object
        doctor = Doctor.objects.get(pk=data.get('doctor'))
        medicine = Medicine.objects.get(name=data.get('medicine'))
        data['patient'] = patient.id
        data['doctor'] = doctor.id
        data['medicine'] = medicine.id
        serializer = PrescriptionSerializer(data=data)
        if serializer.is_valid():
            prescription = serializer.save()
            return JsonResponse({'message': 'Prescription added successfully','prescription':PrescriptionSerializer(prescription).data}, status=201)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


#check prescription by patient id
@csrf_exempt
def check_prescription(request, patient_id):
    if request.method == 'GET':
        prescriptions = Prescription.objects.filter(patient_id=patient_id)
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return JsonResponse({'prescription': serializer.data}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


#show all prerscriptions
@csrf_exempt
def show_prescriptions(request):
    if request.method == 'GET':
        prescriptions = Prescription.objects.all()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return JsonResponse({'prescriptions': serializer.data}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

#get patient information by id
@csrf_exempt
def get_patient(request, customer_id):
    if request.method == 'GET':
        try:
            customer = Customer.objects.get(pk=customer_id)
            serializer = CustomerSerializer(customer)
            return JsonResponse(serializer.data, status=200)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
        return JsonResponse({'error': 'Invalid Request Method'}, status=400)

#show all patients information
@csrf_exempt
def show_patients(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

#generate bill
@csrf_exempt
def create_medical_order(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        appointment_id = data.get('appointment_id')
        medical_expense = data.get('medical_expense')

        #check if appointment_id and medical_expense are both provided
        if appointment_id is None or medical_expense is None:
            return JsonResponse(resposeBody(400,"Bad Request: appointment_id and medical_expense are required", None), status=400)

        #check if appointment_id exists
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return JsonResponse({'message': 'appointment does not exist'}, status=404)

        #check if the appointment has been paid
        existing_oder = MedicalOrder.objects.filter(appointment_id=appointment)
        if existing_oder.exists():
            return JsonResponse(resposeBody(403, 'payment already exists for this appointment', None), status=403)

        #check if is_claim shoude be true or false
        is_claim = False
        if appointment.patient.claim_rate !=0:
            is_claim = True
        try:
            print('creating medicalOrder with appointment_id',appointment_id,'and medical_expense:',medical_expense)
            MedicalOrder.objects.create(
                appointment_id=appointment,
                medical_expense=medical_expense,
                is_claim=is_claim
            )
            return JsonResponse(resposeBody(200, 'created successfully', {
                'appointment_id': appointment_id,
                'medical_expense': medical_expense
            }),status=200)
        except Exception as e:
            print('Exception occoured:',e)
            return JsonResponse({'message':'Failed to create'}, status=500)
    else:
        #not post method
        return JsonResponse({'message':'method not allowed'}, status=405)

#check order by appointment_id
@csrf_exempt
def get_medical_order(request, appointment_id):
        if request.method == 'GET':
            try:
                medical_order = MedicalOrder.objects.filter(appointment_id=appointment_id)
                if not medical_order:
                    return JsonResponse({'error':'MedicalOrder not found'}, status=404)
                serializer = OrderSerializer(medical_order, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Invalid Request Method'}, status=400)


#pay
@csrf_exempt
def pay(request):
    if request.method == 'POST':
        #data = JSONParser().parse(request)
        data = json.loads(request.body)
        customer_id = data['customer_id']
        order_id = data['order_id']

        try:
            #get record
            customer = Customer.objects.get(id=customer_id)
            order = MedicalOrder.objects.get(id=order_id)
            #check expense
            expense = order.medical_expense
            #check balance
            balance = customer.balance
            claim_rate = customer.claim_rate
            if expense>balance:
                return JsonResponse(resposeBody(502, 'insufficient balance!', None))
            if order.is_pay:
                return JsonResponse(resposeBody(502, 'You have paid! ', None))
            #pay
            balance -= (1 - claim_rate)* expense
            #update balance
            customer.balance = balance
            customer.save()
            #modify is_pay
            order.is_pay = True
            order.save()
            customer_data = serialize('json',[customer])
            return JsonResponse(resposeBody(200, 'Your balance is ' + str(balance) + '.', json.loads(customer_data)))
        except Exception:
            return JsonResponse(resposeBody(500, 'failure', json.loads(customer_data)))
#
# #claim
# @csrf_exempt
# def claim(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         #receive patient_ID
#         #receive order_ID
#         customer_id = data['customer_id']
#         order_id = data['order_id']
#         # 获取对应记录
#         customer = Customer.objects.get(id=customer_id)
#         order = MedicalOrder.objects.get(id=order_id)
#         # 查询费用
#         if not customer.is_insurance:
#             return JsonResponse(resposeBody(500, "You don't have available insurance yet", None))
#         if not order.is_pay:
#             return JsonResponse(resposeBody(500, 'You have not completed the payment.', None))
#         if order.is_claim:
#             return JsonResponse(resposeBody(500, 'You have already made a claim.', None))
#
#         expense = order.medical_expense
#         claim_rate = customer.claim_rate
#         balance = customer.balance
#         balance = balance +  (balance * claim_rate / 100)
#         # 更新余额
#         customer.balance = balance
#         customer.save()
#         # 更新索赔状态
#         order.is_claim = True
#         order.save()
#         return JsonResponse(resposeBody(200, 'Claim successful.' + 'Your balance is ' + str(balance) + '.', None))
#
#     return JsonResponse(resposeBody(404, 'Not found!', None))
