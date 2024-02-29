package data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class DoctorIn(
    @SerialName("doctor_id")
    val doctorId: Int,
    @SerialName("last_name")
    val lastName: String,
    @SerialName("first_name")
    val firstName: String,
    @SerialName("middle_name")
    val middleName: String?=null,
    val experience: Int,
    @SerialName("quit_clinic")
    val quitClinic: Boolean=false,
    @SerialName("category_name")
    val categoryName: String,
    @SerialName("speciality_name")
    val specialityName: String,
)
