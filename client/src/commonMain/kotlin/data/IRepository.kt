package data

import data.models.*

interface IRepository {
    suspend fun readVisitByVisitId(visitId: Int): List<VisitDetailed>

    suspend fun createVisit(visit: VisitOut): Int

    suspend fun updateVisit(visitId: Int, updateVisit: VisitUpdate): Int

    suspend fun deleteVisit(visitId: Int): Int

    suspend fun readDoctors(): List<DoctorIn>

    suspend fun createDoctor(doctor: DoctorOut): Int

    suspend fun readVisitsByDoctorId(doctorId: Int): List<DoctorVisitIn>

    suspend fun readPatients(): List<PatientIn>

    suspend fun createPatient(patient: PatientOut): Int

    suspend fun readVisitingSessionsByPatientId(patientId: Int): List<VisitingSession>

    suspend fun readVisits(sessionId: Int): List<PatientVisitIn>

    suspend fun createVisitingSessionByPatientId(patientId: Int): Int

    suspend fun readDiagnoses(): List<BaseItem>

    suspend fun readClinicServices():List<ClinicService>

    suspend fun readPatientCategories(): List<PatientCategory>

    suspend fun readDoctorCategories(): List<BaseItem>

    suspend fun readDoctorSpecialities(): List<BaseItem>

    suspend fun getToken(username: String, password: String): JWTToken
}