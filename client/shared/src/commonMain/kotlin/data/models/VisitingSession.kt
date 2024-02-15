package mk1morebugs.data.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable


@Serializable
data class VisitingSession(
    @SerialName("session_id")
    val sessionId: Int,
    @SerialName("date_start")   // example: 2019-08-24T14:15:22Z
    val dateTimeStart: String,
    @SerialName("date_end")
    val dateTimeEnd: String,       // example: 2019-08-24T14:15:22Z
    @SerialName("sum_price")
    val sumPrice: Int,
    )

