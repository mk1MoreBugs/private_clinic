package data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class PatientVisitIn(
    @SerialName("visit_id")
    val visitId: Int,
    @SerialName("appointment_datetime")
    val appointmentDatetime: String,  // example: 2019-08-24T14:15:22Z
    @SerialName("discounted_price")
    val discountedPrice: Int,
    @SerialName("service_name")
    val serviceName: String,
    @SerialName("doctor_last_name")
    val doctorLastName: String,
    @SerialName("doctor_first_name")
    val doctorFirstName: String,
    @SerialName("doctor_middle_name")
    val doctorMiddleName: String?=null,
    @SerialName("category_name")
    val categoryName: String,
    @SerialName("speciality_name")
    val specialityName: String,



    )
