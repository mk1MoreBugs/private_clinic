package mk1morebugs.viewModels

import data.IRepository
import data.Repository
import data.models.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import mk1morebugs.appCoroutineScope
import mk1morebugs.appState


data class PatientVisitsData(
    val fetchData: Boolean = false,
    val visits: List<PatientVisitIn> = listOf(),
    val clinicServices: List<ClinicService> = listOf(),
    val doctors: List<DoctorIn> = listOf(),
    val diagnoses: List<BaseItem> = listOf(),
    val errorMessage: String? = null,
)


class PatientVisitsViewModel(private val repository: IRepository = Repository()) {
    private val _uiState = MutableStateFlow(PatientVisitsData())
    val uiState: StateFlow<PatientVisitsData> = _uiState.asStateFlow()

    init {
        appCoroutineScope.launch {
            getData()
        }
    }

    private suspend fun getData() {
        _uiState.update {
            it.copy(
                fetchData = true,
            )
        }

        console.log("fetch visits")
        if (appState.value.sessionId != null) {
            _uiState.update {
                it.copy(
                    visits = repository.readVisits(appState.value.sessionId!!),
                    clinicServices = repository.readClinicServices(),
                    doctors = repository.readDoctors().filter { doctor ->
                        !doctor.quitClinic
                    },
                    diagnoses = repository.readDiagnoses(),
                    fetchData = false,
                )
            }
        } else {
            _uiState.update {
                it.copy(
                    errorMessage = "sessionId is null!",
                    fetchData = false,
                )
            }
        }
    }


    suspend fun createVisit(visitOut: VisitOut) {
        console.log("create session")
        repository.createVisit(visitOut)
    }
}
