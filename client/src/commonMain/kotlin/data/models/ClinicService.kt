package data.models

data class ClinicService(
    val id: Int,
    val name: String,
    val price: Int,
    val available: Boolean=true,
)
