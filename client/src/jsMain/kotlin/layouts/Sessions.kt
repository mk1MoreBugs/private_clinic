package mk1morebugs.layouts

import data.ktorClient.Routers
import data.models.VisitingSession
import io.ktor.client.plugins.*
import io.kvision.core.*
import io.kvision.html.button
import io.kvision.html.div
import io.kvision.html.span
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
import mk1morebugs.appState
import mk1morebugs.router
import mk1morebugs.viewModels.SessionsData
import mk1morebugs.viewModels.SessionsViewModel


fun SimplePanel.sessions() {
    val viewModel = SessionsViewModel()
    val uiState = viewModel.uiState

    vPanel {
        gridSessions(uiState)
        createSession(viewModel)
    }
}


private fun VPanel.gridSessions(uiState: StateFlow<SessionsData>) {
    gridPanel(
        columnGap = uiState.value.sessions.size + 1,
        rowGap = 4,
        justifyItems = JustifyItems.CENTER,
        useWrappers = true,
        alignItems = AlignItems.CENTER,
    ).bind(uiState) {

        if (uiState.value.sessions.isNotEmpty()) {
            options(1, 1) {
                div {
                    span("Начало")
                    marginBottom = 20.pt
                }
            }
            options(2, 1) {
                div {
                    span("Конец")
                    marginBottom = 20.pt
                }
            }
            options(3, 1) {
                div {
                    span("Сумма")
                    marginBottom = 20.pt
                }
            }
        }

        for ((index: Int, item: VisitingSession) in uiState.value.sessions.withIndex()) {
            options(1, index + 2) {
                div {
                    span(item.dateTimeStart ?: "Записей ещё нет")
                    marginTop = 15.pt
                    marginBottom = 15.pt
                }
            }
            options(2, index + 2) {
                span(item.dateTimeEnd)
            }
            options(3, index + 2) {
                span((item.sumPrice ?: 0).toString().plus(" ₽"))
            }

            options(4, index + 2) {
                div {
                    paddingTop = 5.pt
                    paddingBottom = 5.pt
                    button(
                        text = "Посмотреть посещения",
                        icon = "bi bi-clock-history",
                    ).onClick {
                        router.navigateToPath(Routers.SESSION.url.plus(item.sessionId))
                    }
                }
            }
        }
    }
}


private fun VPanel.createSession(viewModel: SessionsViewModel) {

    button(
        text = "Добавить сессию"
    ) {
        marginTop = 10.pt
        marginLeft = 30.perc
        marginRight = 30.perc

    }.onClickLaunch {
        try {
            if (appState.value.patientId != null) {
                viewModel.createSession(appState.value.patientId!!)
            }
        } catch (e: ResponseException) {
            ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                message = "Не удалось создать сессию, ${e.message}",
                color = BsColor.DANGER,
            )
        }
    }
}