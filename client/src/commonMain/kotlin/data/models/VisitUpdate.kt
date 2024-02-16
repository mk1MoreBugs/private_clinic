package data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class VisitUpdate(
    @SerialName("appointment_datetime")
    val appointmentDatetime: String?=null,  // example: 2019-08-24T14:15:22Z
    @SerialName("diagnosis_id")
    val diagnosisId: Int?=null,
    val anamnesis: String?=null,
    val opinion: String?=null,

)
