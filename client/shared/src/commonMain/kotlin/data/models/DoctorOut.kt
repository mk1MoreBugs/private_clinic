package data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class DoctorOut(
    @SerialName("last_name")
    val lastName: String,
    @SerialName("first_name")
    val firstName: String,
    @SerialName("middle_name")
    val middleName: String?=null,
    val experience: Int,
    @SerialName("speciality_id")
    val specialityId: Int,
    @SerialName("category_id")
    val categoryId: Int,
)
