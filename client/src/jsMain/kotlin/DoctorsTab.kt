package mk1morebugs

import io.kvision.html.span
import io.kvision.panel.SimplePanel
import io.kvision.panel.vPanel

class DoctorsTab : SimplePanel() {

    init {
        vPanel {
            span ("Doctors")
        }
    }
}