package data

import data.ktorClient.RequestResponse
import data.models.*
import io.ktor.client.call.*
import mk1morebugs.data.ktorClient.Routers

class Repository : IRepository {
    override suspend fun readVisitByVisitId(visitId: Int): List<VisitDetailed> {
        TODO("Not yet implemented")
    }

    override suspend fun createVisit(visit: VisitOut) {
        TODO("Not yet implemented")
    }

    override suspend fun updateVisit(updateVisit: VisitUpdate) {
        TODO("Not yet implemented")
    }

    override suspend fun deleteVisit(visitId: Int) {
        TODO("Not yet implemented")
    }

    override suspend fun readDoctors(): List<DoctorIn> {
        TODO("Not yet implemented")
    }

    override suspend fun createDoctor(doctor: DoctorOut) {
        TODO("Not yet implemented")
    }

    override suspend fun readVisitsByDoctorId(doctorId: Int): List<DoctorVisitIn> {
        TODO("Not yet implemented")
    }

    override suspend fun readPatients(): List<PatientIn> {
        TODO("Not yet implemented")
    }

    override suspend fun createPatient(patient: PatientOut) {
        TODO("Not yet implemented")
    }

    override suspend fun readVisitingSessionsByPatientId(patientId: Int): List<VisitingSession> {
        TODO("Not yet implemented")
    }

    override suspend fun readVisits(sessionId: Int): List<PatientVisitIn> {
        TODO("Not yet implemented")
    }

    override suspend fun createVisitingSessionByPatientId(patientId: Int) {
        TODO("Not yet implemented")
    }

    override suspend fun readDiagnoses(): List<BaseItem> {
        TODO("Not yet implemented")
    }

    override suspend fun readClinicServices(): List<ClinicService> {
        TODO("Not yet implemented")
    }

    override suspend fun readPatientCategories(): List<PatientCategory> {
        TODO("Not yet implemented")
    }

    override suspend fun readDoctorCategories(): List<BaseItem> =
        RequestResponse().getRequest(Routers.DOCTOR_CATEGORIES.url).body()


    override suspend fun readDoctorSpecialities(): List<BaseItem> {
        TODO("Not yet implemented")
    }
}