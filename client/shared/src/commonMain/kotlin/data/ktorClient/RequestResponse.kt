package mk1morebugs.data.ktorClient

import io.ktor.client.*
import io.ktor.client.plugins.contentnegotiation.*
import mk1morebugs.data.Repository
import kotlin.js.json

class RequestResponse : Repository {
    private val client = HttpClient() {
        install(ContentNegotiation) {
            json()
        }
    }


}