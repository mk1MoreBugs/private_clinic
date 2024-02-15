package mk1morebugs.data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class VisitOut(
    @SerialName("appointment_datetime")
    val appointmentDatetime: String,  // example: 2019-08-24T14:15:22Z
    @SerialName("discounted_price")
    val discountedPrice: Int,
    @SerialName("visiting_session_id")
    val visitingSessionId: Int,
    @SerialName("service_id")
    val serviceId: Int,
    @SerialName("diagnosis_id")
    val diagnosisId: Int,
    val anamnesis: String,
    val opinion: String,
)
