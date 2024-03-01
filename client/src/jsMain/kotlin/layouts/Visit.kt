package mk1morebugs.layouts

import io.kvision.core.onClickLaunch
import io.kvision.html.*
import io.kvision.panel.SimplePanel
import io.kvision.panel.hPanel
import io.kvision.panel.vPanel
import io.kvision.state.bind
import io.kvision.utils.pt
import mk1morebugs.appState
import mk1morebugs.viewModels.VisitViewModel

fun SimplePanel.visit() {
    val viewModel = VisitViewModel()
    val uiState = viewModel.uiState

    vPanel().bind(uiState) {
        if (uiState.value.visit.isNotEmpty()) {
            val visit = uiState.value.visit[0]

            hPanel {
                marginBottom = 20.pt
                h1("Visit id: ${visit.visitId}")
                button(
                    text = "Удалить запись",
                    style = ButtonStyle.DANGER
                ) {
                    marginLeft = 30.pt
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
