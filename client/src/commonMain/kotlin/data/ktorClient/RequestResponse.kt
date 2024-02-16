package data.ktorClient

import data.Repository
import data.models.*
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import mk1morebugs.data.ktorClient.Routers


class RequestResponse : Repository {
    private val client = HttpClient() {
        install(ContentNegotiation) {
            json()
        }
    }

    override suspend fun readVisitByVisitId(visitId: Int): List<VisitDetailed> {
        val response: HttpResponse = client.get {
            url {
                host = Routers.host
                path("/visits/".plus(visitId.toString()))
            }
        }
        console.log(response.status.toString())
        return response.body()
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

    override suspend fun readDoctorCategories(): List<BaseItem> {
        val response: HttpResponse = client.get {
            url {
                host = Routers.host
                path("/doctor-categories/")
            }
        }
        console.log(response.status.toString())
        return response.body()
    }

    override suspend fun readDoctorSpecialities(): List<BaseItem> {
        TODO("Not yet implemented")
    }


}