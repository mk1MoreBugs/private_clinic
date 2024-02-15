package mk1morebugs.data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class DoctorVisitIn(
    @SerialName("visit_id")
    val visitId: Int,
    @SerialName("appointment_datetime")
    val appointmentDatetime: String,  // example: 2019-08-24T14:15:22Z
    @SerialName("discounted_price")
    val discountedPrice: Int,
    @SerialName("service_name")
    val serviceName: String,
    @SerialName("patient_last_name")
    val patientLastName: String,
    @SerialName("patient_first_name")
    val patientFirstName: String,
    @SerialName("patient_middle_name")
    val patientMiddleName: String?=null,
)
