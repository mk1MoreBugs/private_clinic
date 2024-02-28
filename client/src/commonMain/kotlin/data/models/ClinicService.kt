package data.models

import kotlinx.serialization.Serializable

@Serializable
data class ClinicService(
    val id: Int,
    val name: String,
    val price: Int,
    val available: Boolean=true,
)
