package mk1morebugs.data.models

import kotlinx.serialization.Serializable


@Serializable
data class BaseItems(  // [/diagnoses, /doctor-categories, /doctor-specialities]
    val id: Int,
    val name: String,
)
