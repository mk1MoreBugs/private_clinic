package mk1morebugs.viewModels

import data.IRepository
import data.Repository
import data.models.VisitingSession
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import mk1morebugs.appCoroutineScope
import mk1morebugs.appState


data class SessionsData(
    val fetchData: Boolean = false,
    val sessions: List<VisitingSession> = listOf(),
)


class SessionsViewModel(private val repository: IRepository = Repository()) {
    private val _uiState = MutableStateFlow(SessionsData())
    val uiState: StateFlow<SessionsData> = _uiState.asStateFlow()

    init {
        appCoroutineScope.launch {
            getData()
        }
    }

    private suspend fun getData() {
        _uiState.update {
            it.copy(
                fetchData = true
            )
        }

        console.log("fetch sessions")
        if (appState.value.patientId != null) {
            _uiState.update {
                it.copy(
                    sessions = repository.readVisitingSessionsByPatientId(appState.value.patientId!!),
                    fetchData = false,
                )
            }
        }
    }


    suspend fun createSession(patientId: Int) {
        console.log("create session")
        repository.createVisitingSessionByPatientId(patientId)
        getData()
    }
}
