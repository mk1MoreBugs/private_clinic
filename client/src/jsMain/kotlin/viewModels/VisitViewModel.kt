package mk1morebugs.viewModels

import data.IRepository
import data.Repository
import data.models.VisitDetailed
import data.models.VisitUpdate
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import mk1morebugs.appCoroutineScope
import mk1morebugs.appState


data class VisitData(
    val fetchData: Boolean = false,
    val visit: List<VisitDetailed> = listOf(),
    val errMessage: String? = null,
)


class VisitViewModel(private val repository: IRepository = Repository()) {
    init {
        appCoroutineScope.launch {
            getData()
        }
    }

    private val _uiState = MutableStateFlow(VisitData())
    val uiState: StateFlow<VisitData> = _uiState.asStateFlow()

    private suspend fun getData() {
        _uiState.update {
            it.copy(
                fetchData = true
            )
        }


        console.log("fetch visit")
        if (appState.value.visitId != null) {
            _uiState.update {
                it.copy(
                    visit = repository.readVisitByVisitId(appState.value.visitId!!),
                    fetchData = false,
                )
            }
            console.log("close fetch visit")
        } else {
            _uiState.update {
                it.copy(
                    errMessage = "visitId is null",
                    fetchData = false,
                )
            }
        }
    }


    suspend fun updateVisit(visitId: Int, update: VisitUpdate) {
        console.log("update...")
        repository.updateVisit(visitId, update)
        getData()
    }


    suspend fun deleteVisit(visitId: Int) {
        console.log("delete...")
        repository.deleteVisit(visitId)
        getData()
    }
}