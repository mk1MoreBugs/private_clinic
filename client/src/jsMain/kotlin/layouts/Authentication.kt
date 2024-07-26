package mk1morebugs.layouts

import io.kvision.core.BsBgColor
import io.kvision.core.BsColor
import io.kvision.core.onClickLaunch
import io.kvision.form.formPanel
import io.kvision.form.text.Password
import io.kvision.form.text.Text
import io.kvision.html.Button
import io.kvision.html.InputType
import io.kvision.i18n.I18n.tr
import io.kvision.modal.Modal
import io.kvision.toast.ToastContainer
import io.kvision.toast.ToastContainerPosition
import kotlinx.coroutines.flow.StateFlow
import kotlinx.serialization.Serializable
import mk1morebugs.viewModels.AuthenticationData
import mk1morebugs.viewModels.AuthenticationViewModel


fun Modal.login() {
    val viewModel = AuthenticationViewModel()
    val uiState: StateFlow<AuthenticationData> =  viewModel.uiState
    @Serializable
    data class AuthenticationForm(
        val userId: String? = null,
        val password: String? = null,
    )

    val requiredMessage = "Поле обязательно!"

    val formPanel = formPanel<AuthenticationForm> {
        add(
            AuthenticationForm::userId,
            Text(
                type = InputType.TEXT,
                label = "user id:",
                maxlength = 50,
            ),
            required = true,
            requiredMessage = requiredMessage,
        )
        add(
            AuthenticationForm::password,
            Password(
                label = tr("password:"), floating = true
            ),
            validatorMessage = { tr("Password is short") },
            required = true,
            requiredMessage = requiredMessage,
        ) {
        (it.getValue()?.length ?: 0) >= 8
        }

    }

    this.add(
        formPanel
    )
    this.addButton(Button("Войти") {
        onClickLaunch {
            if (formPanel.validate()) {
                try {
                    viewModel.updateUiState(
                        username = formPanel.getData().userId
                            ?: throw IllegalArgumentException("поле \"user dd\" обязательно"),
                        password = formPanel.getData().password
                            ?: throw IllegalArgumentException("поле \"password\" обязательно"),
                    )

                    viewModel.sendPasswordAndGetToken()
                } catch (error: IllegalArgumentException) {
                    viewModel.updateErrorMessage(error)
                }
            }
            if (uiState.value.errorMessage != null) {
                ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                    message = uiState.value.errorMessage!!,
                    bgColor = BsBgColor.DANGER,
                    color = BsColor.DANGERBG,
                )
            }
        }
    }
    )
    this.addButton(Button("Сменить пароль")) // todo

    this.show()
}