package mk1morebugs

import data.ktorClient.Routers
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow

data class AppState(
    val views: Routers = Routers.PATIENTS,
    val patientId: Int? = null,
    val doctorId: Int? = null,
    val sessionId: Int? = null,
    val visitId: Int? = null,
)

val appState = MutableStateFlow(AppState())

val appCoroutineScope = CoroutineScope(Dispatchers.Default + SupervisorJob())
