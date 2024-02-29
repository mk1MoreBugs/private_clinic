package mk1morebugs.layouts

import data.ktorClient.Routers
import data.models.PatientVisitIn
import data.models.VisitOut
import io.ktor.client.plugins.*
import io.kvision.core.*
import io.kvision.form.formPanel
import io.kvision.form.select.Select
import io.kvision.form.text.Text
import io.kvision.form.text.TextArea
import io.kvision.form.time.DateTime
import io.kvision.html.*
import io.kvision.modal.Modal
import io.kvision.modal.ModalSize
import io.kvision.panel.*
import io.kvision.state.bind
import io.kvision.toast.ToastContainer
import io.kvision.toast.ToastContainerPosition
import io.kvision.utils.perc
import io.kvision.utils.pt
import kotlinx.coroutines.flow.StateFlow
import kotlinx.serialization.Contextual
import kotlinx.serialization.Serializable
import mk1morebugs.appState
import mk1morebugs.viewModels.PatientVisitsData
import mk1morebugs.viewModels.PatientVisitsViewModel
import kotlin.js.Date


fun SimplePanel.patientVisits() {
    val viewModel = PatientVisitsViewModel()
    val uiState = viewModel.uiState

    vPanel {
        gridVisits(uiState)
        createVisit(uiState, viewModel)
    }
}


private fun VPanel.gridVisits(uiState: StateFlow<PatientVisitsData>) {
    gridPanel(
        columnGap = 30,
        rowGap = 20,
        justifyItems = JustifyItems.CENTER,
        useWrappers = true,
        alignItems = AlignItems.CENTER,
    ).bind(uiState) {

        if (uiState.value.visits.isNotEmpty()) {
            options(1, 1) {
                div {
                    span("id")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(2, 1) {
                div {
                    span("Дата")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(3, 1) {
                div {
                    span("Время")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(4, 1) {
                div {
                    span("Сумма, ₽")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(5, 1) {
                div {
                    span("процент скидки, %")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(6, 1) {
                div {
                    span("Услуга")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(7, 1) {
                div {
                    span("Доктор")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
        }

        for ((index: Int, item: PatientVisitIn) in uiState.value.visits.withIndex()) {
            options(1, index + 2) {
                link(
                    label = item.visitId.toString(),
                    url = "#/".plus(Routers.VISITS.url).plus(item.visitId),
                )
            }
            options(2, index + 2) {
                span(item.appointmentDatetime.slice(0..9))
            }
            options(3, index + 2) {
                span(item.appointmentDatetime.slice(11..15))
            }
            options(4, index + 2) {
                span(item.discountedPrice.toString())
            }
            options(5, index + 2) {
                span((item.discountPercentage ?: 0).toString())
            }
            options(6, index + 2) {
                span(item.serviceName)
            }
            options(7, index + 2) {
                hPanel {
                    span(
                        "${item.doctorLastName} " +
                                "${item.doctorFirstName} " +
                                "${item.doctorMiddleName ?: ""},"
                    ) {
                        paddingRight = 10.pt
                    }
                    span(item.categoryName.plus(",")) {
                        paddingRight = 10.pt
                    }
                    span(item.specialityName)
                }
            }

        }

    }
}


private fun VPanel.createVisit(uiState: StateFlow<PatientVisitsData>, viewModel: PatientVisitsViewModel) {
    @Serializable
    data class VisitForm(
        @Contextual val appointmentDate: Date? = null,
        @Contextual val appointmentTime: Date? = null,
        val discountedPrice: String? = null,
        val clinicServiceId: String? = null,
        val doctorId: String? = null,
        val diagnosisId: String? = null,
        val anamnesis: String? = null,
        val opinion: String? = null,
    )

    val requiredMessage = "Поле обязательно!"

    button(
        text = "Добавить посещение"
    ) {
        marginTop = 10.pt
        marginLeft = 30.perc
        marginRight = 30.perc
        icon = "bi bi-plus-square"

    }.onClick {
        val modal = Modal("Создание посещения")

        val formPanel = formPanel<VisitForm> {
            add(
                VisitForm::appointmentDate,
                DateTime(format = "YYYY-MM-DD", label = "Дата посещения"),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                VisitForm::appointmentTime,
                DateTime(format = "HH:mm", label = "Время посещения"),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                VisitForm::discountedPrice,
                Text(
                    type = InputType.TEXT,
                    label = "Сумма",
                ),
                required = true,
                requiredMessage = requiredMessage,
                validatorMessage = { "Сумма должна быть целым числом" }
            ) {
                it.getValue()?.let { inputPrice ->
                    "^\\d+$".toRegex().matches(inputPrice)
                }
            }
            add(
                VisitForm::clinicServiceId,
                Select(
                    options = uiState.value.clinicServices.map { it.id.toString() to it.name },
                    label = "Название услуги"
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                VisitForm::doctorId,
                Select(
                    options = uiState.value.doctors.map {
                        it.doctorId.toString() to
                                "${it.lastName} ${it.firstName} ${it.middleName ?: ""}"
                    },
                    label = "Доктор"
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                VisitForm::diagnosisId,
                Select(
                    options = uiState.value.diagnoses.map { it.id.toString() to it.name },
                    label = "Диагноз"
                ),
                required = false,
            )
            add(
                VisitForm::anamnesis,
                TextArea(
                    label = "Анамнез",
                    rows = 10,
                ),
                required = false,
            )
            add(
                VisitForm::opinion,
                TextArea(
                    label = "Заключение",
                    rows = 15,
                ),
                required = false,
            )
        }


        modal.size = ModalSize.XLARGE
        modal.add(
            formPanel
        )

        modal.addButton(Button("Добавить запись") {
            onClickLaunch {
                console.log("adding...")


                formPanel.validate()
                try {
                    val appointmentDatetime: String =
                        formPanel.getData().appointmentDate?.toISOString()?.slice(0..9)?.plus(
                            formPanel.getData().appointmentTime?.toISOString()?.slice(10..15)
                        ) ?: throw IllegalArgumentException("поля \"Дата\" и \"Время\" обязательны")

                    val price = formPanel.getData().discountedPrice?.toInt()
                        ?: throw IllegalArgumentException("ошибка в поле \"Сумма\"")

                    viewModel.createVisit(
                        visitOut = VisitOut(
                            discountedPrice = price,

                            visitingSessionId = appState.value.sessionId
                                ?: throw IllegalArgumentException("sessionId is null"),

                            serviceId = formPanel.getData().clinicServiceId?.toInt()
                                ?: throw IllegalArgumentException("ошибка в поле \"Название услуги\""),

                            doctorId = formPanel.getData().doctorId?.toInt()
                                ?: throw IllegalArgumentException("ошибка в поле \"Доктор\""),

                            appointmentDatetime = appointmentDatetime,
                            diagnosisId = formPanel.getData().diagnosisId?.toInt(),
                            anamnesis = formPanel.getData().anamnesis,
                            opinion = formPanel.getData().opinion,
                        )
                    )
                    modal.hide()

                } catch (e: IllegalArgumentException) {
                    ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                        message = "Не удалось создать запись, ${e.message}",
                        bgColor = BsBgColor.DANGER,
                        color = BsColor.DANGERBG,
                    )
                } catch (e: ResponseException) {
                    ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                        message = "Не удалось создать запись, ${e.message}",
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
