package data.models

import kotlinx.serialization.Serializable


@Serializable
data class BaseItem(  // [/diagnoses, /doctor-categories, /doctor-specialities]
    val id: Int,
    val name: String,
)
