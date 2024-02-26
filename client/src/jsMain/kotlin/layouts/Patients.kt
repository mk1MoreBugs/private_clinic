package mk1morebugs.layouts

import data.ktorClient.Routers
import data.models.PatientIn
import data.models.PatientOut
import io.ktor.client.plugins.*
import io.kvision.core.*
import io.kvision.form.formPanel
import io.kvision.form.select.Select
import io.kvision.form.text.Text
import io.kvision.form.time.DateTime
import io.kvision.html.*
import io.kvision.modal.Modal
import io.kvision.panel.SimplePanel
import io.kvision.panel.VPanel
import io.kvision.panel.gridPanel
import io.kvision.panel.vPanel
import io.kvision.state.bind
import io.kvision.toast.ToastContainer
import io.kvision.toast.ToastContainerPosition
import io.kvision.utils.perc
import io.kvision.utils.pt
import kotlinx.coroutines.flow.StateFlow
import kotlinx.serialization.Contextual
import kotlinx.serialization.Serializable
import mk1morebugs.router
import mk1morebugs.viewModels.PatientsData
import mk1morebugs.viewModels.PatientsViewModel
import kotlin.js.Date


fun SimplePanel.patients() {
    val viewModel = PatientsViewModel()
    val uiState = viewModel.uiState

    vPanel {
        gridPatients(uiState)
        createPatient(uiState, viewModel)
    }
}

private fun VPanel.gridPatients(uiState: StateFlow<PatientsData>) {
    gridPanel(
        columnGap = uiState.value.patients.size + 1,
        rowGap = 7,
        justifyItems = JustifyItems.CENTER,
        useWrappers = true,
        alignItems = AlignItems.CENTER,
    ).bind(uiState) {

        if (uiState.value.patients.isNotEmpty()) {
            options(1, 1) {
                div {
                    span("Фамилия")
                    marginBottom = 20.pt
                }
            }
            options(2, 1) {
                div {
                    span("Имя")
                    marginBottom = 20.pt
                }
            }
            options(3, 1) {
                div {
                    span("Отчество")
                    marginBottom = 20.pt
                }
            }
            options(4, 1) {
                div {
                    span("Дата рождения")
                    marginBottom = 20.pt
                }
            }
            options(5, 1) {
                div {
                    span("Категория пациента")
                    marginBottom = 20.pt
                }
            }
        }

        for ((index: Int, item: PatientIn) in uiState.value.patients.withIndex()) {
            options(1, index + 2) {
                div {
                    span(item.lastName)
                    marginTop = 15.pt
                    marginBottom = 15.pt
                }
            }
            options(2, index + 2) {
                span(item.firstName)
            }
            options(3, index + 2) {
                span(item.middleName)
            }
            options(4, index + 2) {
                span(item.birthday)
            }
            options(5, index + 2) {
                span(item.categoryName ?: "Нет категории")
            }
            options(6, index + 2) {
                div {
                    paddingTop = 5.pt
                    paddingBottom = 5.pt
                    button(
                        text = "Посмотреть сессии обращений",
                        icon = "bi bi-clock-history",
                    ).onClick {
                        router.navigateToPath(Routers.PATIENTS.url.plus(item.patientId))
                    }
                }
            }
        }
    }
}


private fun VPanel.createPatient(uiState: StateFlow<PatientsData>, viewModel: PatientsViewModel) {
    @Serializable
    data class PatientForm(
        val lastName: String? = null,
        val firstName: String? = null,
        val middleName: String? = null,
        @Contextual val birthday: Date? = null,
        val categoryId: String? = null,
    )

    val requiredMessage = "Поле обязательно!"

    button(
        text = "Добавить пациента"
    ) {
        marginTop = 10.pt
        marginLeft = 30.perc
        marginRight = 30.perc
        icon = "bi bi-person-plus-fill"

    }.onClick {
        val modal = Modal("Создание пациента")

        val formPanel = formPanel<PatientForm> {
            add(
                PatientForm::lastName,
                Text(
                    type = InputType.TEXT,
                    label = "Фамилия",
                    maxlength = 50,
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                PatientForm::firstName,
                Text(
                    type = InputType.TEXT,
                    label = "Имя",
                    maxlength = 50,
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                PatientForm::middleName,
                Text(
                    type = InputType.TEXT,
                    label = "Отчество",
                    maxlength = 50,
                ),
                required = false,
            )
            add(
                PatientForm::birthday,
                DateTime(format = "YYYY-MM-DD", label = "Дата рождения"),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                PatientForm::categoryId,
                Select(
                    options = uiState.value.patientCategories.map { it.id.toString() to it.name },
                    label = "Категория пациента"
                ),
                required = false,
            )
        }

        modal.add(
            formPanel
        )

        modal.addButton(Button("Добавить пациента") {
            onClickLaunch {
                console.log("adding...")

                formPanel.validate()
                try {
                    if (formPanel.getData().birthday == null) {
                        throw IllegalArgumentException("поле \"Дата рождения\" обязательно")
                    }
                    val dateString: String = formPanel.getData().birthday!!.toISOString().slice(IntRange(0, 9))

                    viewModel.createPatient(
                        patient = PatientOut(
                            lastName = formPanel.getData().lastName
                                ?: throw IllegalArgumentException("поле \"Фамилия\" обязательно"),

                            firstName = formPanel.getData().firstName
                                ?: throw IllegalArgumentException("поле \"Имя\" обязательно"),

                            middleName = formPanel.getData().middleName,
                            birthday = dateString,
                            categoryId = formPanel.getData().categoryId?.toInt(),
                        )
                    )
                    modal.hide()

                } catch (e: IllegalArgumentException) {
                    ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                        message = "Не удалось создать пациента, ${e.message}",
                        bgColor = BsBgColor.DANGER,
                        color = BsColor.DANGERBG,
                    )
                } catch (e: ResponseException) {
                    ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                        message = "Не удалось создать пациента, ${e.message}",
                        color = BsColor.DANGER,
                    )
                }
            }
        })

        modal.addButton(Button("Закрыть") {
            onClick {
                modal.hide()
                console.log("modal close")
            }
        })
        modal.show()
    }
}
