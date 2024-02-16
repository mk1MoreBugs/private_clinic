package data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class PatientIn(
    @SerialName("patient_id")
    val patientId: Int,
    @SerialName("last_name")
    val lastName: String,
    @SerialName("first_name")
    val firstName: String,
    @SerialName("middle_name")
    val middleName: String?=null,
    @SerialName("birthday")
    val birthday: String,
    @SerialName("category_name")
    val categoryName: String,
    @SerialName("category_id")
    val categoryId: Int,
)
