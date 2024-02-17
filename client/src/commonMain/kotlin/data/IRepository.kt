package data

import data.models.*

interface IRepository {
    suspend fun readVisitByVisitId(visitId: Int): List<VisitDetailed>

    suspend fun createVisit(visit: VisitOut)

    suspend fun updateVisit(updateVisit: VisitUpdate)

    suspend fun deleteVisit(visitId: Int)

    suspend fun readDoctors(): List<DoctorIn>

    suspend fun createDoctor(doctor: DoctorOut)

    suspend fun readVisitsByDoctorId(doctorId: Int): List<DoctorVisitIn>

    suspend fun readPatients(): List<PatientIn>

    suspend fun createPatient(patient: PatientOut)

    suspend fun readVisitingSessionsByPatientId(patientId: Int): List<VisitingSession>

    suspend fun readVisits(sessionId: Int): List<PatientVisitIn>

    suspend fun createVisitingSessionByPatientId(patientId: Int)

    suspend fun readDiagnoses(): List<BaseItem>

    suspend fun readClinicServices():List<ClinicService>

    suspend fun readPatientCategories(): List<PatientCategory>

    suspend fun readDoctorCategories(): List<BaseItem>

    suspend fun readDoctorSpecialities(): List<BaseItem>
}