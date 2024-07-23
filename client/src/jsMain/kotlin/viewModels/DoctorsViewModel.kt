package mk1morebugs.viewModels

import data.IRepository
import data.Repository
import data.ktorClient.NetworkErrorException
import data.models.BaseItem
import data.models.DoctorIn
import data.models.DoctorOut
import io.ktor.client.plugins.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import mk1morebugs.appCoroutineScope


data class DoctorsData(
    val fetchData: Boolean = false,
    val doctors: List<DoctorIn> = listOf(),
    val doctorCategories: List<BaseItem> = listOf(),
    val doctorSpecialities: List<BaseItem> = listOf(),
)


class DoctorsViewModel(private val repository: IRepository = Repository()) {
    init {
        appCoroutineScope.launch {
            getData()
        }
    }

    private val _uiState = MutableStateFlow(DoctorsData())
    val uiState: StateFlow<DoctorsData> = _uiState.asStateFlow()

    private suspend fun getData() {
        _uiState.update {
            it.copy(
                fetchData = true
            )
        }
        console.log("fetch doctors")
        try {
            _uiState.update {
                it.copy(
                    doctors = repository.readDoctors(),
                    doctorCategories = repository.readDoctorCategories(),
                    doctorSpecialities = repository.readDoctorSpecialities(),
                )
            }
        } catch (error: ClientRequestException) {
            printErrorMessage(error)
        } catch (error: ServerResponseException) {
            printErrorMessage(error)
        } catch (error: NetworkErrorException) {
            printErrorMessage(error)
        }  finally {
            _uiState.update {
                it.copy(
                    fetchData = false,
                )
            }
        }

    }


    suspend fun createDoctor(doctor: DoctorOut) {
        console.log("create...")
        repository.createDoctor(doctor)
        getData()
    }


    private fun printErrorMessage(error: Exception) {
        println("error message: ${error.message}")
    }
}
