plugins {
    alias(libs.plugins.kotlin.multiplatform)
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
        }
        binaries.executable()
    }


    sourceSets {
        jsMain.dependencies {
            implementation(libs.kvision)
            implementation(libs.kvision.bootstrap)
            implementation(libs.kvision.i18n)
            implementation(libs.kvision.routing.navigo.ng)
            implementation(npm("css-loader", "6.10.0"))

            implementation(libs.ktor.client.js)
        }

        jsTest.dependencies {
            implementation(kotlin("test-js"))
            implementation(libs.kvision.testutils)
        }
    }
}