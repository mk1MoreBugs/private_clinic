package mk1morebugs.layouts

import data.ktorClient.Routers
import data.models.DoctorIn
import data.models.DoctorOut
import io.ktor.client.plugins.*
import io.kvision.core.*
import io.kvision.form.formPanel
import io.kvision.form.select.Select
import io.kvision.form.text.Text
import io.kvision.html.*
import io.kvision.modal.Modal
import io.kvision.panel.SimplePanel
import io.kvision.panel.VPanel
import io.kvision.panel.gridPanel
import io.kvision.panel.vPanel
import io.kvision.state.bind
import io.kvision.toast.ToastContainer
import io.kvision.toast.ToastContainerPosition
import io.kvision.utils.perc
import io.kvision.utils.pt
import kotlinx.coroutines.flow.StateFlow
import kotlinx.serialization.Serializable
import mk1morebugs.router
import mk1morebugs.viewModels.DoctorsData
import mk1morebugs.viewModels.DoctorsViewModel


fun SimplePanel.doctors() {
    val viewModel = DoctorsViewModel()
    val uiState = viewModel.uiState

    vPanel {
        gridDoctors(uiState)
        createDoctor(uiState, viewModel)
    }
}


private fun VPanel.gridDoctors(uiState: StateFlow<DoctorsData>) {
    gridPanel(
        columnGap = 30,
        rowGap = 20,
        justifyItems = JustifyItems.CENTER,
        useWrappers = true,
        alignItems = AlignItems.CENTER,
    ).bind(uiState) {

        if (uiState.value.doctors.isNotEmpty()) {
            options(1, 1) {
                div {
                    span("Фамилия")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(2, 1) {
                div {
                    span("Имя")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(3, 1) {
                div {
                    span("Отчество")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(4, 1) {
                div {
                    span("Специальность")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(5, 1) {
                div {
                    span("Категория")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
            options(6, 1) {
                div {
                    span("Уволен")
                    marginBottom = 10.pt
                    marginRight = 15.pt
                    marginLeft = 15.pt
                }
            }
        }

        for ((index: Int, item: DoctorIn) in uiState.value.doctors.withIndex()) {
            options(1, index + 2) {
                span(item.lastName)
            }
            options(2, index + 2) {
                span(item.firstName)
            }
            options(3, index + 2) {
                span(item.middleName ?: "")
            }
            options(4, index + 2) {
                span(item.specialityName)
            }
            options(5, index + 2) {
                span(item.categoryName)
            }
            options(6, index + 2) {

                span(item.quitClinic.let {
                    if (it) {
                        "Да"
                    }
                    else {
                        "Нет"
                    }
                })
            }
            options(7, index + 2) {
                div {
                    button(
                        text = "Посмотреть обращения пациентов",
                        icon = "bi bi-clock-history",
                    ).onClick {
                        router.navigateToPath(Routers.DOCTORS.url.plus(item.doctorId))
                    }
                }
            }
        }
    }
}


private fun VPanel.createDoctor(uiState: StateFlow<DoctorsData>, viewModel: DoctorsViewModel) {
    @Serializable
    data class DoctorForm(
        val lastName: String? = null,
        val firstName: String? = null,
        val middleName: String? = null,
        val experience: String? = null,
        val specialityId: String? = null,
        val categoryId: String? = null,
    )

    val requiredMessage = "Поле обязательно!"

    button(
        text = "Создать доктора"
    ) {
        marginTop = 30.pt
        marginLeft = 30.perc
        marginRight = 30.perc
        icon = "bi bi-person-plus-fill"

    }.onClick {
        val modal = Modal("Создание доктора")

        val formPanel = formPanel<DoctorForm> {
            add(
                DoctorForm::lastName,
                Text(
                    type = InputType.TEXT,
                    label = "Фамилия",
                    maxlength = 50,
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                DoctorForm::firstName,
                Text(
                    type = InputType.TEXT,
                    label = "Имя",
                    maxlength = 50,
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                DoctorForm::middleName,
                Text(
                    type = InputType.TEXT,
                    label = "Отчество",
                    maxlength = 50,
                ),
                required = false,
            )
            add(
                DoctorForm::experience,
                Text(
                    type = InputType.TEXT,
                    label = "Опыт работы",
                ),
                required = true,
                requiredMessage = requiredMessage,
                validatorMessage = { "Сумма должна быть целым числом от 0 до 100" }
            ) {
                it.getValue()?.let { inputPrice ->
                    "^\\d..$".toRegex().matches(inputPrice)
                }
            }
            add(
                DoctorForm::specialityId,
                Select(
                    options = uiState.value.doctorCategories.map { it.id.toString() to it.name },
                    label = "Категория"
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
            add(
                DoctorForm::categoryId,
                Select(
                    options = uiState.value.doctorSpecialities.map { it.id.toString() to it.name },
                    label = "Специальность"
                ),
                required = true,
                requiredMessage = requiredMessage,
            )
        }

        modal.add(
            formPanel
        )

        modal.addButton(Button("Добавить доктора") {
            onClickLaunch {
                console.log("adding...")

                formPanel.validate()
                try {
                    val experience = formPanel.getData().experience?.toInt()
                        ?: throw IllegalArgumentException("поле \"Опыт работы\" обязательно")
                    if (experience < 0 || experience > 100 ) {
                        throw IllegalArgumentException("Сумма должна быть целым числом от 0 до 100")
                    }

                    viewModel.createDoctor(
                        doctor = DoctorOut(
                            lastName = formPanel.getData().lastName
                                ?: throw IllegalArgumentException("поле \"Фамилия\" обязательно"),

                            firstName = formPanel.getData().firstName
                                ?: throw IllegalArgumentException("поле \"Имя\" обязательно"),

                            middleName = formPanel.getData().middleName,

                            experience = formPanel.getData().experience?.toInt()
                                ?: throw IllegalArgumentException("поле \"Опыт работы\" обязательно"),

                            specialityId = formPanel.getData().specialityId?.toInt()
                                ?: throw IllegalArgumentException("поле \"Категория\" обязательно"),

                            categoryId = formPanel.getData().categoryId?.toInt()
                                ?: throw IllegalArgumentException("поле \"Специальность\" обязательно"),
                        )
                    )
                    modal.hide()

                } catch (e: IllegalArgumentException) {
                    ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                        message = "Не удалось создать доктора, ${e.message}",
                        bgColor = BsBgColor.DANGER,
                        color = BsColor.DANGERBG,
                    )
                } catch (e: ResponseException) {
                    ToastContainer(ToastContainerPosition.TOPCENTER).showToast(
                        message = "Не удалось создать доктора, ${e.message}",
                        color = BsColor.DANGER,
                    )
                }
            }
        })

        modal.addButton(Button("Закрыть") {
            onClick {
                modal.hide()
                console.log("modal close")
            }
        })
        modal.show()
    }
}
