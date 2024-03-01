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


data class VisitsData(
    val fetchData: Boolean = false,
    val patientVisits: List<PatientVisitIn> = listOf(),
    val doctorVisits: List<DoctorVisitIn> = listOf(),
    val clinicServices: List<ClinicService> = listOf(),
    val doctors: List<DoctorIn> = listOf(),
    val diagnoses: List<BaseItem> = listOf(),
    val errorMessage: String? = null,
)


class VisitsViewModel(private val repository: IRepository = Repository()) {
    private val _uiState = MutableStateFlow(VisitsData())
    val uiState: StateFlow<VisitsData> = _uiState.asStateFlow()

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

        val patientVisits = if (appState.value.sessionId != null) {
            repository.readVisits(appState.value.sessionId!!)
        } else listOf()

        val doctorVisits = if (appState.value.doctorId != null) {
            repository.readVisitsByDoctorId(appState.value.doctorId!!)
        } else listOf()

        _uiState.update {
            it.copy(
                patientVisits = patientVisits,
                doctorVisits = doctorVisits,
                clinicServices = repository.readClinicServices(),
                doctors = repository.readDoctors().filter { doctor ->
                    !doctor.quitClinic
                },
                diagnoses = repository.readDiagnoses(),
                fetchData = false,
            )
        }
    }


    suspend fun createVisit(visitOut: VisitOut) {
        console.log("create session")
        repository.createVisit(visitOut)
        getData()
    }
}
