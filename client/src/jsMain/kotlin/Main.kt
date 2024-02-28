package mk1morebugs

import io.kvision.*
import io.kvision.html.*
import io.kvision.navbar.nav
import io.kvision.navbar.navLink
import io.kvision.navbar.navbar
import io.kvision.panel.*
import io.kvision.state.bind
import io.kvision.theme.Theme
import io.kvision.theme.ThemeManager
import io.kvision.utils.perc
import io.kvision.utils.pt
import mk1morebugs.layouts.doctors
import mk1morebugs.layouts.patients
import mk1morebugs.layouts.sessions
import mk1morebugs.layouts.patientVisits


class App : Application() {
    init {
        ThemeManager.init(initialTheme = Theme.DARK, remember = true)
    }

    override fun start() {
        router.initRoutes().resolve()
        val appState = appState

        root("kvapp") {

            navbar("Private Clinic") {
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
                    else -> {
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
