package mk1morebugs.viewModels

import data.IRepository
import data.Repository
import data.ktorClient.NetworkErrorException
import io.ktor.client.plugins.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import mk1morebugs.appState


data class AuthenticationData(
    val userId: String? = null,
    val password: String? = null,
    val errorMessage: String? = null
)


class AuthenticationViewModel(private val repository: IRepository = Repository()) {
    private val _uiState = MutableStateFlow(AuthenticationData())
    val uiState: StateFlow<AuthenticationData> = _uiState.asStateFlow()

    fun updateUiState(username: String, password: String) {
        _uiState.update {
            it.copy(
                userId = username,
                password = password,
            )
        }
    }

    suspend fun sendPasswordAndGetToken() {
        try {
            repository.getToken(username = uiState.value.userId!!, password = uiState.value.password!!)
            appState.update {
                it.copy(
                    userId = uiState.value.userId?.toInt()
                )
            }
        } catch (error: ClientRequestException) {
            updateErrorMessage(error)
        } catch (error: NetworkErrorException) {
            updateErrorMessage(error)
        }
    }


    fun updateErrorMessage(error: Exception?) {
        _uiState.update {
            it.copy(
                errorMessage = error?.message
            )
        }
    }
}