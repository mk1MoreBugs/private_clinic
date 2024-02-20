package mk1morebugs

import io.kvision.*
import io.kvision.panel.*
import io.kvision.routing.Routing
import io.kvision.theme.Theme
import io.kvision.theme.ThemeManager


class App : Application() {
    init {
        ThemeManager.init(initialTheme = Theme.DARK, remember = true)
        Routing.init()
    }

    override fun start() {
        root("kvapp") {


            tabPanel {
                addTab("Basic formatting", PatientsTab(), route = "/patients")
                addTab("Forms", DoctorsTab(), route = "/doctors")
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
