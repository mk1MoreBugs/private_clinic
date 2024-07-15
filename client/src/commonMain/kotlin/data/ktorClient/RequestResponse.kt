package data.ktorClient

import io.ktor.client.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.client.plugins.auth.*
import io.ktor.client.plugins.auth.providers.*


class RequestResponse {
    private val client = HttpClient {
        install(ContentNegotiation) {
            json()
        }

        install(Auth) {
            bearer {
                loadTokens {
                    // Load tokens from a local storage and return them as the 'BearerTokens' instance
                    BearerTokens("abc123", "xyz111")
                }
                refreshTokens { // this: RefreshTokensParams
                    // Refresh tokens and return them as the 'BearerTokens' instance
                    BearerTokens("def456", "xyz111")
                }

            }
        }

        expectSuccess = true
        HttpResponseValidator{
            handleResponseExceptionWithRequest { exception, _ ->
                val clientException = exception as? ClientRequestException ?: return@handleResponseExceptionWithRequest
                val exceptionResponse = clientException.response
                val exceptionResponseText = exceptionResponse.bodyAsText()
                if (exceptionResponse.status.value / 100 == 4) {
                    throw ClientRequestException(exceptionResponse, exceptionResponseText)
                }
                if (exceptionResponse.status.value / 100 == 5) {
                    throw ServerResponseException(exceptionResponse, exceptionResponseText)
                }
            }

        }
    }


    suspend fun getRequest(url: String): HttpResponse {
        val response: HttpResponse = client.get {
            url {
                host = Routers.HOST.url
                path(url)
            }
        }

        console.log(response.status.toString())
        return response
    }


    suspend fun postRequest(url: String, data: Any): HttpResponse {
        val response: HttpResponse = client.post {
            url {
                host = Routers.HOST.url
                path(url)
            }
            contentType(ContentType.Application.Json)
            setBody(data)
        }

        console.log(response.status.toString())
        return response
    }


    suspend fun deleteRequest(url: String): HttpResponse {
        val response: HttpResponse = client.delete {
            url {
                host = Routers.HOST.url
                path(url)
            }
        }

        console.log(response.status.toString())
        return response
    }


    suspend fun putRequest(url: String, data: Any): HttpResponse {
        val response: HttpResponse = client.put {
            url {
                host = Routers.HOST.url
                path(url)
            }
            contentType(ContentType.Application.Json)
            setBody(data)
        }

        console.log(response.status.toString())
        return response
    }
}