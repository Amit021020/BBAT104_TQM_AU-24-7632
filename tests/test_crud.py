import unittest

from app.services.patient_service import (
    create_patient,
    get_all_patients,
    update_patient,
    delete_patient,
)

from app.services.doctor_service import (
    create_doctor,
    get_all_doctors,
    update_doctor,
    delete_doctor,
)

from app.services.appointment_service import (
    create_appointment,
    get_all_appointments,
    update_appointment,
    delete_appointment,
)

from app.services.medical_record_service import (
    create_medical_record,
    get_all_medical_records,
    update_medical_record,
    delete_medical_record,
)

from app.services.bill_service import (
    create_bill,
    get_all_bills,
    update_bill,
    delete_bill,
)

from app.services.user_service import (
    create_user,
    get_all_users,
    update_user,
    delete_user,
)


class TestCRUD(unittest.TestCase):

    def test_patient_crud(self):
        patient_id = create_patient({
            "patient_code": "TEST-P001",
            "name": "Test Patient",
            "age": 25,
            "gender": "Male",
            "blood_group": "O+",
            "phone": "9999999999",
            "address": "Test Address",
            "emergency_contact": "8888888888",
        })

        self.assertIsNotNone(patient_id)

        patients = get_all_patients()
        self.assertTrue(any(p["id"] == patient_id for p in patients))

        updated = update_patient(
            patient_id,
            {
                "patient_code": "TEST-P001",
                "name": "Updated Patient",
                "age": 26,
                "gender": "Male",
                "blood_group": "O+",
                "phone": "9999999999",
                "address": "Updated Address",
                "emergency_contact": "8888888888",
            },
        )

        self.assertTrue(updated)

        deleted = delete_patient(patient_id)
        self.assertTrue(deleted)

    def test_doctor_crud(self):
        doctor_id = create_doctor({
            "doctor_code": "TEST-D001",
            "name": "Test Doctor",
            "specialization": "General Medicine",
            "department": "General",
            "phone": "9999999998",
            "email": "testdoctor@example.com",
        })

        self.assertIsNotNone(doctor_id)

        doctors = get_all_doctors()
        self.assertTrue(any(d["id"] == doctor_id for d in doctors))

        updated = update_doctor(
            doctor_id,
            {
                "doctor_code": "TEST-D001",
                "name": "Updated Doctor",
                "specialization": "Cardiology",
                "department": "Cardiology",
                "phone": "9999999998",
                "email": "updated@example.com",
            },
        )

        self.assertTrue(updated)

        deleted = delete_doctor(doctor_id)
        self.assertTrue(deleted)

    def test_appointment_crud(self):
        patient_id = create_patient({
            "patient_code": "TEST-AP-P001",
            "name": "Appointment Patient",
            "age": 30,
            "gender": "Female",
            "blood_group": "A+",
            "phone": "9999999997",
            "address": "Test Address",
            "emergency_contact": "8888888887",
        })

        doctor_id = create_doctor({
            "doctor_code": "TEST-AP-D001",
            "name": "Appointment Doctor",
            "specialization": "General Medicine",
            "department": "General",
            "phone": "9999999996",
            "email": "appointment@example.com",
        })

        appointment_id = create_appointment({
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": "2026-10-08",
            "appointment_time": "10:00",
            "reason": "Regular checkup",
            "status": "Scheduled",
        })

        self.assertIsNotNone(appointment_id)

        appointments = get_all_appointments()
        self.assertTrue(
            any(a["id"] == appointment_id for a in appointments)
        )

        updated = update_appointment(
            appointment_id,
            {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_date": "2026-10-09",
                "appointment_time": "11:00",
                "reason": "Updated checkup",
                "status": "Completed",
            },
        )

        self.assertTrue(updated)

        deleted = delete_appointment(appointment_id)
        self.assertTrue(deleted)

        delete_doctor(doctor_id)
        delete_patient(patient_id)

    def test_medical_record_crud(self):
        patient_id = create_patient({
            "patient_code": "TEST-MR-P001",
            "name": "Medical Record Patient",
            "age": 35,
            "gender": "Male",
            "blood_group": "B+",
            "phone": "9999999995",
            "address": "Test Address",
            "emergency_contact": "8888888885",
        })

        doctor_id = create_doctor({
            "doctor_code": "TEST-MR-D001",
            "name": "Medical Record Doctor",
            "specialization": "Medicine",
            "department": "General",
            "phone": "9999999994",
            "email": "medicalrecord@example.com",
        })

        record_id = create_medical_record({
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "diagnosis": "Fever",
            "prescription": "Paracetamol",
            "notes": "Rest required",
            "record_date": "2026-10-08",
        })

        self.assertIsNotNone(record_id)

        records = get_all_medical_records()
        self.assertTrue(
            any(r["id"] == record_id for r in records)
        )

        updated = update_medical_record(
            record_id,
            {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "diagnosis": "Viral Fever",
                "prescription": "Paracetamol 500mg",
                "notes": "Updated notes",
                "record_date": "2026-10-08",
            },
        )

        self.assertTrue(updated)

        deleted = delete_medical_record(record_id)
        self.assertTrue(deleted)

        delete_doctor(doctor_id)
        delete_patient(patient_id)

    def test_bill_crud(self):
        patient_id = create_patient({
            "patient_code": "TEST-B-P001",
            "name": "Billing Patient",
            "age": 40,
            "gender": "Female",
            "blood_group": "AB+",
            "phone": "9999999993",
            "address": "Test Address",
            "emergency_contact": "8888888883",
        })

        bill_id = create_bill({
            "patient_id": patient_id,
            "amount": 1500.00,
            "payment_status": "Pending",
            "bill_date": "2026-10-08",
        })

        self.assertIsNotNone(bill_id)

        bills = get_all_bills()
        self.assertTrue(
            any(b["id"] == bill_id for b in bills)
        )

        updated = update_bill(
            bill_id,
            {
                "patient_id": patient_id,
                "amount": 1800.00,
                "payment_status": "Paid",
                "bill_date": "2026-10-08",
            },
        )

        self.assertTrue(updated)

        deleted = delete_bill(bill_id)
        self.assertTrue(deleted)

        delete_patient(patient_id)

    def test_user_crud(self):
        user_id = create_user({
            "username": "test_user_crud",
            "password": "test123",
            "role": "Staff",
            "is_active": 1,
        })

        self.assertIsNotNone(user_id)

        users = get_all_users()
        self.assertTrue(
            any(u["id"] == user_id for u in users)
        )

        updated = update_user(
            user_id,
            {
                "username": "updated_test_user",
                "password": "newtest123",
                "role": "Admin",
                "is_active": 1,
            },
        )

        self.assertTrue(updated)

        deleted = delete_user(user_id)
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()