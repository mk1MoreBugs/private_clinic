plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.kotlinx.serialization)
    alias(libs.plugins.kvision)
}


group = "mk1morebugs"
version = "1.0-SNAPSHOT"


repositories {
    mavenCentral()
}


kotlin {
    js {
        browser {
            webpackTask {
                mainOutputFileName = "main.bundle.js"
            }

            testTask {
                enabled = false
            }
        }
        binaries.executable()
    }


    sourceSets {
        jsMain.dependencies {
            implementation(libs.kvision)
            implementation(libs.kvision.bootstrap)
            implementation(libs.kvision.i18n)
            implementation(libs.kvision.routing.navigo.ng)

            implementation(libs.kvision.bootstrap.icons)
            implementation(libs.kvision.datetime)
            implementation(libs.kvision.state)
            implementation(libs.kvision.state.flow)

            implementation(npm("css-loader", "7.1.2"))

            implementation(libs.ktor.client.js)
        }

        jsTest.dependencies {
            implementation(kotlin("test-js"))
            implementation(libs.kvision.testutils)
        }

        commonMain.dependencies {
            implementation(libs.ktor.client.core)
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.ktor.serialization.kotlinx.json)
            implementation(libs.ktor.client.content.negotiation)
            implementation(libs.ktor.client.auth)
        }

        commonTest.dependencies {
            implementation(kotlin("test")) // Brings all the platform dependencies automatically
        }
    }
}