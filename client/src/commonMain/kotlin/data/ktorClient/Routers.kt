package mk1morebugs.data.ktorClient

enum class Routers(val url: String) {
    HOST("localhost:8080"),
    VISITS("/visits/"),
    DOCTORS("/doctors/"),
    PATIENTS("/patients/"),
    SESSION("/session/"),
    DIAGNOSES("/diagnoses"),
    SERVICES("/clinic-services"),
    PATIENT_CATEGORIES("/patient-categories"),
    DOCTOR_CATEGORIES("/doctor-categories"),
    DOCTOR_SPECIALITIES("/doctor-specialities"),



}