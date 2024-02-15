package mk1morebugs.data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class PatientCategory(
    val id: Int,
    val name: String,
    @SerialName("discount_percentage")
    val discountPercentage: Int
)
