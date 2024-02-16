package data.models

import mk1morebugs.data.models.PatientIn
import kotlin.test.Test
import kotlin.test.assertEquals

class TestUserIn {
    private val responseJSON: List<String> = listOf(
        """{"last_name":"Иванов", "first_name":"Иван", "middle_name":"Иванович", "birthday":"2019-08-24", "category_id":0, "patient_id":0, "category_name":"string"}"""
    )
    @Test
    fun deserializeJSON() {
        val obj = kotlinx.serialization.json.Json.decodeFromString<PatientIn>(responseJSON[0])
        val expected = PatientIn(
            patientId = 0,
            lastName = "Иванов",
            firstName = "Иван",
            birthday = "2019-08-24",
            categoryId = 0,
            categoryName = "string",
        )

        assertEquals(expected = expected.patientId, actual = obj.patientId)
    }
}