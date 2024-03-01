package mk1morebugs.viewModels

import data.IRepository
import data.Repository
import data.models.PatientCategory
import data.models.PatientIn
import data.models.PatientOut
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import mk1morebugs.appCoroutineScope

data class PatientsData(
    val fetchData: Boolean = false,
    val patients: List<PatientIn> = listOf(),
    val patientCategories: List<PatientCategory> = listOf(),
)


class PatientsViewModel(private val repository: IRepository = Repository()) {
    init {
        appCoroutineScope.launch {
            getData()
        }
    }

    private val _uiState = MutableStateFlow(PatientsData())
    val uiState: StateFlow<PatientsData> = _uiState.asStateFlow()

    private suspend fun getData() {
        _uiState.update {
            it.copy(
                fetchData = true
            )
        }

        coroutineScope {
            console.log("fetch patients")
            val patientCategories: List<PatientCategory> = repository.readPatientCategories()
            val patients: List<PatientIn> = repository.readPatients()
            _uiState.update {
                it.copy(
                    patients = patients,
                    patientCategories = patientCategories,
                    fetchData = false,
                )
            }
            console.log("close fetch patients")
        }
    }


    suspend fun createPatient(patient: PatientOut) {
        console.log("create...")
        repository.createPatient(patient)
        getData()
    }
}
