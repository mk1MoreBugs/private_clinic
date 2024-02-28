package mk1morebugs

import data.ktorClient.Routers
import io.kvision.navigo.Navigo
import io.kvision.routing.Routing
import kotlinx.coroutines.flow.update
import kotlin.js.RegExp


enum class Views {
    DOCTORS,
    PATIENTS,
    SESSION,
    VISITS,
    VISIT
}


class Router(root: String) {
    private val router = Routing.init(root)

    fun initRoutes(): Navigo {
        console.log(router.root)
        return router.on("/", {
            console.log("route: /")

        }).on(Routers.DOCTORS.url, {
            console.log("route: /doctors")
            appState.update {
                it.copy(
                    views = Views.DOCTORS,
                    patientId = null,
                    sessionId = null,
                    visitId = null,
                )
            }
        }).on(Routers.PATIENTS.url, {
            console.log("route: /patients")
            appState.update {
                it.copy(
                    views = Views.PATIENTS
                )
            }
        }).on(getStringRegExp(Routers.PATIENTS.url), { match ->
            appState.update {
                it.copy(
                    patientId = match.data[0].toString().toInt(),
                    doctorId = null,
                    views = Views.SESSION
                )
            }
            console.log("statePatientId", appState.value.patientId)

        }).on(getStringRegExp(Routers.SESSION.url), { match ->
            appState.update {
                it.copy(
                    sessionId = match.data[0].toString().toInt(),
                    patientId = null,
                    doctorId = null,
                    views = Views.VISITS
                )
            }
            console.log("stateSessionId", appState.value.sessionId)

        }).on(getStringRegExp(Routers.VISITS.url), { match ->
            appState.update {
                it.copy(
                    visitId = match.data[0].toString().toInt(),
                    views = Views.VISIT
                )
            }
            console.log("stateVisitsId: ", appState.value.visitId)
        })
    }


    fun navigateToPath(path: String) {
        router.navigate(path)
    }

    private fun getStringRegExp(string: String): RegExp {
        return RegExp("^${string.drop(1)}([0-9]*)$")
    }

}


val router = Router("/")
