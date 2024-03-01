package mk1morebugs.layouts

import data.models.VisitUpdate
import io.ktor.client.plugins.*
import io.kvision.core.BsBgColor
import io.kvision.core.BsColor
import io.kvision.core.onClickLaunch
import io.kvision.form.formPanel
import io.kvision.form.select.Select
import io.kvision.form.text.TextArea
import io.kvision.form.time.DateTime
import io.kvision.html.*
import io.kvision.modal.Modal
import io.kvision.modal.ModalSize
import io.kvision.panel.SimplePanel
import io.kvision.panel.hPanel
import io.kvision.panel.vPanel
import io.kvision.state.bind
import io.kvision.toast.ToastContainer
import io.kvision.toast.ToastContainerPosition
import io.kvision.utils.pt
import kotlinx.coroutines.flow.StateFlow
import kotlinx.serialization.Contextual
import kotlinx.serialization.Serializable
import mk1morebugs.appState
import mk1morebugs.viewModels.VisitData
import mk1morebugs.viewModels.VisitViewModel
import kotlin.js.Date


fun SimplePanel.visit() {
    val viewModel = VisitViewModel()
    val uiState = viewModel.uiState

    vPanel().bind(uiState) {
        if (uiState.value.visit.isNotEmpty()) {
            val visit = uiState.value.visit[0]

            hPanel {
                marginBottom = 20.pt
                h1("Visit id: ${visit.visitId}")

                updateVisit(uiState, viewModel)

                button(
                    text = "Удалить запись",
                    style = ButtonStyle.DANGER
                ) {
                    size = ButtonSize.SMALL
                    marginLeft = 60.pt
                }.onClickLaunch {
                    if (appState.value.visitId != null) {
                        viewModel.deleteVisit(appState.value.visitId!!)
                    }
                }
            }

            hPanel {
                marginBottom = 10.pt
                span("Название услуги:") {
                    marginRight = 20.pt
                }
                span(visit.serviceName)
            }

            hPanel {
                marginBottom = 10.pt
                span("Цена с учетом скидки:") {
                    marginRight = 20.pt
                }
                span(visit.discountedPrice.toString())
            }

            hPanel {
                marginBottom = 10.pt
                span("Размер скидки:") {
                    marginRight = 20.pt
                }
                span(visit.discountPercentage.toString().plus(" %"))
            }

            hPanel {
                marginBottom = 30.pt
                span("Дата и время:") {
                    marginRight = 20.pt
                }
                span(visit.appointmentDatetime.slice(0..9)) {
                    marginRight = 5.pt
                }
                span(visit.appointmentDatetime.slice(11..15))
            }

            h2("Пациент") {
                marginBottom = 10.pt
            }
            hPanel {
                marginBottom = 10.pt
                span("ФИО:") {
                    marginRight = 20.pt
                }
                span("${visit.patientLastName} ${visit.patientFirstName} ${visit.patientMiddleName ?: ""}")
            }

            hPanel {
                marginBottom = 30.pt
                span("Дата рождения") {
                    marginRight = 20.pt
                }
                span(visit.patientBirthday)
            }

            h2("Доктор") {
                marginBottom = 10.pt
            }
            hPanel {
                marginBottom = 10.pt
                span("ФИО:") {
                    marginRight = 20.pt
                }
                span("${visit.doctorLastName} ${visit.doctorFirstName} ${visit.doctorMiddleName ?: ""}")
            }

            hPanel {
                marginBottom = 10.pt
                span("Опыт работы:") {
                    marginRight = 20.pt
                }
                span(visit.doctorExperience.toString() + " лет")
            }

            hPanel {
                marginBottom = 10.pt
                span("Категория:") {
                    marginRight = 20.pt
                }
                span(visit.categoryName)
            }

            hPanel {
                marginBottom = 30.pt
                span("Специальность:") {
                    marginRight = 20.pt
                }
                span(visit.specialityName)
            }

            h2("Диагноз") {
                marginBottom = 10.pt
            }
            hPanel {
                marginBottom = 10.pt
                span("Название:") {
                    marginRight = 20.pt
                }
                span(visit.diagnosisName ?: "Диагноз не определен")
            }

            span("Анамнез:") {
                marginBottom = 2.pt
                fontSize = 17.pt
            }
            span(visit.anamnesis ?: "Нет данных")

            span("Заключение:") {
                marginTop = 10.pt
                marginBottom = 2.pt
                fontSize = 17.pt
            }
            span(visit.opinion ?: "Нет данных")

        } else {
            span("Нет данных")
        }
    }
}


private fun SimplePanel.updateVisit(uiState: StateFlow<VisitData>, viewModel: VisitViewModel) {
    @Serializable
    data class VisitForm(
        @Contextual val appointmentDate: Date? = null,
        @Contextual val appointmentTime: Date? = null,
        val diagnosisId: String? = null,
        val anamnesis: String? = null,
        val opinion: String? = null,
    )

    button(
        text = "Обновить данные",
        style = ButtonStyle.OUTLINESECONDARY,
    ) {
        size = ButtonSize.SMALL
        marginLeft = 30.pt

    }.onClick {
        val modal = Modal("Обновление данных")

        val formPanel = formPanel<VisitForm> {
            add(
                VisitForm::appointmentDate,
                DateTime(format = "YYYY-MM-DD", label = "Дата посещения"),
            )
            add(
                VisitForm::appointmentTime,
                DateTime(format = "HH:mm", label = "Время посещения"),
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
                    rows = 30,
                ),
                required = false,
            )
            add(
                VisitForm::opinion,
                TextArea(
                    label = "Заключение",
                    rows = 30,
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
                    val appointmentDatetime: String? = if (
                        formPanel.getData().appointmentDate != null
                        && formPanel.getData().appointmentTime == null
                    ) {
                        formPanel.getData().appointmentDate?.toISOString()?.slice(0..9).plus(
                            uiState.value.visit[0].appointmentDatetime.slice(10..15)
                        )
                    } else if (
                        formPanel.getData().appointmentDate == null
                        && formPanel.getData().appointmentTime != null
                    ) {
                        uiState.value.visit[0].appointmentDatetime.slice(0..10).plus(
                            formPanel.getData().appointmentTime?.toLocaleTimeString()
                        )
                    } else if (
                        formPanel.getData().appointmentDate != null
                        && formPanel.getData().appointmentTime != null
                    ) {
                        formPanel.getData().appointmentDate?.toISOString()?.slice(0..10).plus(
                            formPanel.getData().appointmentTime?.toLocaleTimeString()
                        )
                    } else {
                        null
                    }

                    if (appState.value.visitId != null) {
                        viewModel.updateVisit(
                            visitId = appState.value.visitId!!,
                            update = VisitUpdate(
                                appointmentDatetime = appointmentDatetime,
                                diagnosisId = formPanel.getData().diagnosisId?.toInt(),
                                anamnesis = formPanel.getData().anamnesis,
                                opinion = formPanel.getData().opinion,
                            )
                        )
                    }

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

