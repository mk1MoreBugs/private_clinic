plugins {
    val kotlinVersion = "1.9.22"
    val kvisionVersion = "7.3.1"
    kotlin("plugin.serialization") version kotlinVersion
    kotlin("multiplatform") version kotlinVersion
    id("io.kvision") version kvisionVersion
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
        val kvisionVersion = "7.3.1"
        val ktor = "2.3.8"

        jsMain.dependencies {
            implementation("io.kvision:kvision:$kvisionVersion")
            implementation("io.kvision:kvision-bootstrap:$kvisionVersion")
            implementation("io.kvision:kvision-i18n:$kvisionVersion")
            implementation("io.kvision:kvision-routing-navigo-ng:$kvisionVersion")
            implementation(npm("css-loader", "6.10.0"))

            implementation("io.ktor:ktor-client-js:$ktor")
        }

        jsTest.dependencies {
            implementation(kotlin("test-js"))
            implementation("io.kvision:kvision-testutils:$kvisionVersion")
        }


        commonMain.dependencies {
            implementation("io.ktor:ktor-client-core:$ktor")
        }

        commonTest.dependencies {
            implementation(kotlin("test")) // Brings all the platform dependencies automatically
        }
    }
}