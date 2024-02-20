package mk1morebugs

import data.models.PatientIn
import data.models.PatientOut
import io.ktor.client.plugins.*
import io.kvision.core.*
import io.kvision.form.asMap
import io.kvision.form.formPanel
import io.kvision.form.select.Select
import io.kvision.html.*
import io.kvision.modal.Modal
import io.kvision.panel.SimplePanel
import io.kvision.panel.vPanel
import kotlinx.serialization.Serializable
import io.kvision.form.text.Text
import io.kvision.form.time.DateTime
import io.kvision.panel.hPanel
import io.kvision.state.bind
import io.kvision.toast.ToastContainer
import io.kvision.toast.ToastContainerPosition
import io.kvision.utils.perc
import io.kvision.utils.pt
import kotlinx.serialization.Contextual
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
            button(
                text = "fetch",
                style = ButtonStyle.SECONDARY,
                ) {
                marginRight = 90.perc
            }.onClickLaunch {
                viewModel.getData()
                }

            vPanel().bind(uiState) {
                marginRight = 10.perc
                marginLeft = 10.perc

                for (item: PatientIn in uiState.value.patients) {
                    hPanel(
                        justify = JustifyContent.SPACEBETWEEN,
                        wrap = FlexWrap.WRAP,
                        useWrappers = true,
                    ) {

                        span(item.lastName) {
                            marginTop = 10.pt
                            marginRight = 20.pt
                        }
                        span(item.firstName) {
                            marginTop = 10.pt
                            marginRight = 20.pt
                        }
                        span(item.middleName) {
                            marginTop = 10.pt
                            marginRight = 20.pt
                        }
                        span(item.birthday) {
                            marginTop = 10.pt
                            marginRight = 20.pt
                        }
                        span(item.categoryName) {
                            marginTop = 10.pt
                            marginRight = 20.pt
                        }

                        button("Посмотреть сессии обращений") {
                            paddingLeft = 60.pt
                            marginTop = 10.pt
                            marginLeft = 40.pt
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
                    ). also {
                        icon = "bi bi-calendar-date-fill"
                    }
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
                        val dateString: String = formPanel.getDataJson()
                            .asMap()["birthday"].toString().slice(IntRange(0,9))

                        formPanel.validate()
                        try {
                            if (formPanel.getData().birthday == null) {
                                throw IllegalArgumentException("поле \"Дата рождения\" обязательно")
                            }
                            viewModel.createPatient(
                                patient = PatientOut(
                                    lastName = formPanel.getData().lastName ?:
                                    throw IllegalArgumentException("поле \"Фамилия\" обязательно"),

                                    firstName = formPanel.getData().firstName ?:
                                    throw IllegalArgumentException("поле \"Имя\" обязательно"),

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
}
