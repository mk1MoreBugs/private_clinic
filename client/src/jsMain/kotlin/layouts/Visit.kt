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
                h1(visit.visitId.toString())
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
                span("Название услуги:")
                span(visit.serviceName)
            }

            hPanel {
                span("Цена с учетом скидки:")
                span(visit.discountedPrice.toString())
            }

            hPanel {
                span("Размер скидки:")
                span(visit.discountPercentage.toString().plus(" %"))
            }

            hPanel {
                span("Дата и время:") {
                    paddingRight = 10.pt
                }
                span(visit.appointmentDatetime.slice(0..9)) {
                    paddingRight = 5.pt
                }
                span(visit.appointmentDatetime.slice(11..15))
            }

            h2("Пациент")
            hPanel {
                span("ФИО:")
                span("${visit.patientLastName} ${visit.patientFirstName} ${visit.patientMiddleName ?: ""}")
            }

            hPanel {
                span("Дата рождения")
                span(visit.patientBirthday)
            }

            h2("Доктор")
            hPanel {
                span("ФИО:")
                span("${visit.doctorLastName} ${visit.doctorFirstName} ${visit.doctorMiddleName ?: ""}")
            }

            hPanel {
                span("Опыт работы:")
                span(visit.doctorExperience.toString() + " лет")
            }

            hPanel {
                span("Категория:")
                span(visit.categoryName)
            }

            hPanel {
                span("Специальность:")
                span(visit.specialityName)
            }

            h2("Диагноз")
            hPanel {
                span("Название:")
                span(visit.diagnosisName ?: "Диагноз не определен")
            }

            span("Анамнез:")
            span(visit.anamnesis ?: "Нет данных")

            span("Заключение:")
            span(visit.opinion ?: "Нет данных")

        } else {
            span("Нет данных")
        }
    }
}