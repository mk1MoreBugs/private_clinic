package mk1morebugs

import io.kvision.*
import io.kvision.html.div
import io.kvision.html.span
import io.kvision.modal.Modal
import io.kvision.navbar.nav
import io.kvision.navbar.navLink
import io.kvision.navbar.navbar
import io.kvision.panel.root
import io.kvision.state.bind
import io.kvision.theme.Theme
import io.kvision.theme.ThemeManager
import io.kvision.utils.perc
import io.kvision.utils.pt
import mk1morebugs.layouts.*


class App : Application() {
    init {
        ThemeManager.init(initialTheme = Theme.DARK, remember = true)
    }

    override fun start() {
        router.initRoutes().resolve()
        val appState = appState

        root("kvapp") {

            navbar("Private Clinic").bind(appState) {
                nav {
                    navLink(
                        label = "Patients",
                        url = "#/patients",
                        icon = "bi bi-person-lines-fill",
                    )

                    navLink(
                        label = "Doctors",
                        url = "#/doctors",
                        icon = "bi bi-clipboard2-pulse-fill",
                        )

                    if (appState.value.userId == null) {
                        navLink(
                            label = "Login",
                            url = "#/login",
                        )
                    } else {
                        navLink(
                            label = "user ID: ${appState.value.userId}",
                             url = "#/user-id/${appState.value.userId}",
                        )
                    }
                }
            }

            div().bind(appState) {
                marginTop = 10.pt
                marginRight = 10.perc
                marginLeft = 10.perc

                when (appState.value.views) {
                    Views.PATIENTS -> patients()
                    Views.DOCTORS -> doctors()
                    Views.SESSION -> sessions()
                    Views.VISITS -> patientVisits()
                    Views.VISIT -> visit()
                    Views.AUTHENTICATION -> Modal(caption = "Login").login()
                    Views.NOT_FOUND -> {
                        span("Страница не найдена!")
                    }
                }
            }
        }
    }


    override fun dispose(): Map<String, Any> {
        return mapOf()
    }

}


fun main() {
    startApplication(
        ::App,
        module.hot,
        CoreModule,
        BootstrapModule,
        BootstrapIconsModule,
        DatetimeModule,
    )
    console.log("Hello, Kotlin/JS!")
}
