package data

import data.ktorClient.RequestResponse
import data.models.*
import io.ktor.client.call.*
import data.ktorClient.Routers

class Repository : IRepository {
    private val request = RequestResponse()
    override suspend fun readVisitByVisitId(visitId: Int): List<VisitDetailed> = request.getRequest(
        url = Routers.VISITS.url.plus(visitId)
    ).body()


    override suspend fun createVisit(visit: VisitOut): Int = request.postRequest(
        url = Routers.VISITS.url,
        data = visit
    ).status.value


    override suspend fun updateVisit(visitId: Int, updateVisit: VisitUpdate): Int = request.putRequest(
        url = Routers.VISITS.url.plus("update/").plus(visitId),
        data = updateVisit
    ).status.value


    override suspend fun deleteVisit(visitId: Int): Int = request.deleteRequest(
        url = Routers.VISITS.url.plus("delete/").plus(visitId)
    ).status.value


    override suspend fun readDoctors(): List<DoctorIn> = request.getRequest(
        url = Routers.DOCTORS.url
    ).body()


    override suspend fun createDoctor(doctor: DoctorOut): Int = request.postRequest(
        url = Routers.DOCTORS.url,
        data = doctor
    ).status.value


    override suspend fun readVisitsByDoctorId(doctorId: Int): List<DoctorVisitIn> = request.getRequest(
        url = Routers.DOCTORS.url.plus(doctorId)
    ).body()


    override suspend fun readPatients(): List<PatientIn> = request.getRequest(
        url = Routers.PATIENTS.url
    ).body()


    override suspend fun createPatient(patient: PatientOut): Int = request.postRequest(
        url = Routers.PATIENTS.url,
        data = patient
    ).status.value


    override suspend fun readVisitingSessionsByPatientId(patientId: Int): List<VisitingSession> = request.getRequest(
        url = Routers.PATIENTS.url.plus(patientId)
    ).body()


    override suspend fun readVisits(sessionId: Int): List<PatientVisitIn> = request.getRequest(
        Routers.SESSION.url.plus(sessionId)
    ).body()


    override suspend fun createVisitingSessionByPatientId(patientId: Int): Int = request.postRequest(
        url = Routers.SESSION.url.plus("create/"),
        data = patientId
    ).status.value


    override suspend fun readDiagnoses(): List<BaseItem> = request.getRequest(
        url = Routers.DIAGNOSES.url
    ).body()


    override suspend fun readClinicServices(): List<ClinicService> = request.getRequest(
        url = Routers.SERVICES.url
    ).body()


    override suspend fun readPatientCategories(): List<PatientCategory> = request.getRequest(
        url = Routers.PATIENT_CATEGORIES.url
    ).body()


    override suspend fun readDoctorCategories(): List<BaseItem> = request.getRequest(
        url = Routers.DOCTOR_CATEGORIES.url
    ).body()


    override suspend fun readDoctorSpecialities(): List<BaseItem> = request.getRequest(
        url = Routers.DOCTOR_SPECIALITIES.url
    ).body()

    override suspend fun getToken(username: String, password: String) {
        request.getToken(username=username, password = password)
    }
}
