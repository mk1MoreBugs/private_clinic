package mk1morebugs.layouts

import io.kvision.html.span
import io.kvision.panel.SimplePanel
import io.kvision.panel.vPanel


fun SimplePanel.visits() {
    vPanel {
       span("Visits")
        span("[not implemented yet]")
    }
}