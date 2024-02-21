package mk1morebugs

import data.models.PatientIn
import data.models.PatientOut
import io.ktor.client.plugins.*
import io.kvision.core.BsBgColor
import io.kvision.core.BsColor
import io.kvision.core.JustifyItems
import io.kvision.core.onClickLaunch
import io.kvision.form.formPanel
import io.kvision.form.select.Select
import io.kvision.form.text.Text
import io.kvision.form.time.DateTime
import io.kvision.html.*
import io.kvision.modal.Modal
import io.kvision.panel.SimplePanel
import io.kvision.panel.gridPanel
import io.kvision.panel.vPanel
import io.kvision.state.bind
import io.kvision.toast.ToastContainer
import io.kvision.toast.ToastContainerPosition
import io.kvision.utils.perc
import io.kvision.utils.pt
import kotlinx.serialization.Contextual
import kotlinx.serialization.Serializable
import kotlin.js.Date


@Serializable
data class PatientForm(
    val lastName: String? = null,
    val firstName: String? = null,
    val middleName: String? = null,
    @Contextual val birthday: Date? = null,
    val categoryId: String? = null,
)


class PatientsTab : SimplePanel() {
    private val viewModel = PatientsViewModel()
    private val uiState = viewModel.uiState

    private val requiredMessage = "Поле обязательно!"


    init {
        vPanel {
            marginRight = 10.perc
            marginLeft = 10.perc

            button(
                text = "fetch",
                style = ButtonStyle.SECONDARY,
                icon = "bi bi-arrow-repeat",
            ) {
                marginRight = 90.perc
                marginTop = 5.pt
            }.onClickLaunch {
                viewModel.getData()
            }

            gridPanel(
                columnGap = uiState.value.patients.size + 1,
                rowGap = 7,
                justifyItems = JustifyItems.CENTER,
                useWrappers = true,
            ).bind(uiState) {

                if (uiState.value.patients.isNotEmpty()) {
                    options(1, 1) {
                        div {
                            span("Фамилия")
                            marginBottom = 30.pt
                        }

                    }
                    options(2, 1) {
                        div {
                            span("Имя")
                            marginBottom = 30.pt
                        }

                    }
                    options(3, 1) {
                        div {
                            span("Отчество")
                            marginBottom = 30.pt
                        }

                    }
                    options(4, 1) {
                        div {
                            span("Дата рождения")
                            marginBottom = 30.pt
                        }

                    }
                    options(5, 1) {
                        div {
                            span("Категория пациента")
                            marginBottom = 30.pt
                        }

                    }
                }

                for ((index: Int, item: PatientIn) in uiState.value.patients.withIndex()) {
                    options(1, index + 2) {
                        div().styleGrid {
                            span(item.lastName)
                        }
                    }
                    options(2, index + 2) {
                        div().styleGrid {
                            span(item.firstName)
                        }
                    }
                    options(3, index + 2) {
                        div().styleGrid {
                            span(item.middleName)
                        }
                    }
                    options(4, index + 2) {
                        div().styleGrid {
                            span(item.birthday)
                        }
                    }
                    options(5, index + 2) {
                        div().styleGrid {
                            span(item.categoryName ?: "Нет категории")
                        }
                    }
                    options(6, index + 2) {
                        div {
                            button(
                                text = "Посмотреть сессии обращений",
                                icon = "bi bi-clock-history",
                            )
                            marginBottom = 15.pt
                        }
                    }
                }
            }

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
    }


    private fun Div.styleGrid(function: () -> SimplePanel) {
        function()
        marginBottom = 15.pt
    }
}