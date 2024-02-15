plugins {
    alias(libs.plugins.kotlinx.serialization)
    alias(libs.plugins.kotlin.multiplatform)
}


repositories {
    mavenCentral()
}


kotlin {
    js {
       browser{
           testTask {
               enabled = false
           }
       }
    }

    sourceSets {
        commonMain.dependencies {
            implementation(libs.ktor.client.core)
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.ktor.serialization.kotlinx.json)
            implementation(libs.ktor.client.content.negotiation)
        }

        commonTest.dependencies {
            implementation(kotlin("test")) // Brings all the platform dependencies automatically
        }
    }
}