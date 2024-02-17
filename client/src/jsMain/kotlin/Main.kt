package mk1morebugs

import data.Repository
import io.kvision.*
import io.kvision.core.*
import io.kvision.html.button
import io.kvision.html.span
import io.kvision.panel.hPanel
import io.kvision.panel.root
import io.kvision.panel.vPanel
import io.kvision.theme.Theme
import io.kvision.theme.ThemeManager
import io.kvision.utils.pt


class App : Application() {
    init {
        ThemeManager.init(initialTheme = Theme.DARK, remember = false)

    }

    override fun start() {

        // val routing = Routing.init()
        root("kvapp") {

            hPanel {
                paddingTop = 10.pt
                spacing = 10
                justifyContent = JustifyContent.CENTER

                color = Color.name(Col.BLUE)
                background = Background(color = Color.name(Col.RED))

                span("Hello world")
                button("click me!").also {
                    onClickLaunch {
                        val listObj = Repository().readDoctorCategories()

                        for (item in listObj) {
                            console.log("clk!")
                            console.log(item.name)

                            span(item.id.toString())
                            span(item.name)
                        }




                    }
                }
            }
            vPanel {
                alignItems = AlignItems.END

                span("Hello world")
                span("Hello world")

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
    )
    console.log("Hello, Kotlin/JS!")
}