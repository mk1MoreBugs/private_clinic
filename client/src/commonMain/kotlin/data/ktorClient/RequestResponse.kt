package data.ktorClient

import data.models.JWTToken
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.client.plugins.auth.*
import io.ktor.client.plugins.auth.providers.*
import io.ktor.client.request.forms.*


val bearerTokenStorage: MutableList<BearerTokens> = mutableListOf(
    BearerTokens(
        accessToken="",
        refreshToken = "",
    )
)


class RequestResponse {


    private val client = HttpClient {
        install(ContentNegotiation) {
            json()
        }

        install(Auth) {
            bearer {
                loadTokens {
                    bearerTokenStorage.last()
                }
                refreshTokens {
                    bearerTokenStorage.last()
                }
                sendWithoutRequest { request ->
                    request.url.host == Routers.HOST.url
                }
            }
        }

        expectSuccess = true
        HttpResponseValidator{
            handleResponseExceptionWithRequest { exception, _ ->
                println("exception!")
                println("cause: ${exception.cause}, message: ${exception.message}")

                // throw NetworkError Exception when NetworkError is happened
                val exceptionCause = exception.cause?.toString() ?: ""
                if ("NetworkError" in exceptionCause) {
                    throw NetworkErrorException(message = exception.message!!)
                }

                val clientException = exception as? ResponseException ?: return@handleResponseExceptionWithRequest
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

    suspend fun getToken(
        username: String,
        password: String,
    ): JWTToken {
        val token: JWTToken = client.submitForm (
            url = "http://".plus(Routers.HOST.url).plus("/authorization/token"),
            formParameters = parameters {
                append("username", username)
                append("password", password)
            }
        ).body()
        bearerTokenStorage.add(BearerTokens(accessToken = token.accessToken, refreshToken = ""))

        return token
    }
}