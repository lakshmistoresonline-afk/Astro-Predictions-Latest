package com.astro.predictions.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.astro.predictions.data.model.*
import com.astro.predictions.data.repository.AstrovisionRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed class AstrovisionUiState {
    object Idle : AstrovisionUiState()
    data class Loading(val message: String) : AstrovisionUiState()
    data class Success(val response: BirthProfileResponse) : AstrovisionUiState()
    data class Error(val message: String) : AstrovisionUiState()
}

sealed class AiInterpretationUiState {
    object Idle : AiInterpretationUiState()
    object Loading : AiInterpretationUiState()
    data class Success(val domain: String, val interpretation: String, val validationStatus: String) : AiInterpretationUiState()
    data class Error(val message: String) : AiInterpretationUiState()
}

enum class NavigationTab(val label: String) {
    FORM("Birth Profile"),
    DASHBOARD("Dashboard"),
    KUNDALI("Kundali Chart"),
    PLANETS("Planetary Positions"),
    VARGAS("16 Vargas"),
    DASHAS("Vimshottari Dashas"),
    YOGAS_DOSHAS("Yogas & Doshas"),
    STRENGTH("Shadbala & SAV"),
    JAIMINI("Jaimini Karakas"),
    PANCHANGA("Panchanga & Muhurta"),
    PREDICTIONS("14 Domain Predictions"),
    AI_INTERPRETATION("AI Interpretation")
}

class AstrovisionViewModel(
    private val repository: AstrovisionRepository = AstrovisionRepository()
) : ViewModel() {

    private val _uiState = MutableStateFlow<AstrovisionUiState>(AstrovisionUiState.Idle)
    val uiState: StateFlow<AstrovisionUiState> = _uiState.asStateFlow()

    private val _aiUiState = MutableStateFlow<AiInterpretationUiState>(AiInterpretationUiState.Idle)
    val aiUiState: StateFlow<AiInterpretationUiState> = _aiUiState.asStateFlow()

    private val _activeTab = MutableStateFlow(NavigationTab.FORM)
    val activeTab: StateFlow<NavigationTab> = _activeTab.asStateFlow()

    // Form inputs initialized clean (no fake/sample name or preloaded profile)
    val nameState = MutableStateFlow("")
    val yearState = MutableStateFlow(2000)
    val monthState = MutableStateFlow(1)
    val dayState = MutableStateFlow(1)
    val hourState = MutableStateFlow(12)
    val minuteState = MutableStateFlow(0)
    val selectedCityIndexState = MutableStateFlow(0)
    val timezoneStrState = MutableStateFlow(PRESET_CITIES[0].tz)
    val placeNameState = MutableStateFlow(PRESET_CITIES[0].name)
    val countryState = MutableStateFlow(PRESET_CITIES[0].country)
    val latitudeState = MutableStateFlow(PRESET_CITIES[0].lat)
    val longitudeState = MutableStateFlow(PRESET_CITIES[0].lon)

    fun onCitySelected(index: Int) {
        if (index in PRESET_CITIES.indices) {
            val city = PRESET_CITIES[index]
            selectedCityIndexState.value = index
            placeNameState.value = city.name
            countryState.value = city.country
            latitudeState.value = city.lat
            longitudeState.value = city.lon
            timezoneStrState.value = city.tz
        }
    }

    fun selectTab(tab: NavigationTab) {
        _activeTab.value = tab
    }

    fun calculateBirthProfile() {
        val name = nameState.value.trim()
        if (name.isEmpty()) {
            _uiState.value = AstrovisionUiState.Error("Please enter your full birth name.")
            return
        }

        viewModelScope.launch {
            _uiState.value = AstrovisionUiState.Loading("Connecting to NASA JPL DE440s Ephemeris Backend...")

            val request = BirthProfileRequest(
                name = name,
                year = yearState.value,
                month = monthState.value,
                day = dayState.value,
                hour = hourState.value,
                minute = minuteState.value,
                second = 0,
                timezoneStr = timezoneStrState.value,
                latitude = latitudeState.value,
                longitude = longitudeState.value,
                placeName = placeNameState.value,
                country = countryState.value
            )

            val result = repository.calculateBirthProfile(request)
            result.fold(
                onSuccess = { response ->
                    _uiState.value = AstrovisionUiState.Success(response)
                    _activeTab.value = NavigationTab.DASHBOARD
                },
                onFailure = { error ->
                    _uiState.value = AstrovisionUiState.Error(
                        error.localizedMessage ?: "Failed to connect to backend engine. Ensure FastAPI server is running."
                    )
                }
            )
        }
    }

    fun interpretDomainAi(domainCode: String, prompt: String = "Explain the Parashari domain factors and planetary influences.") {
        val currentState = _uiState.value
        if (currentState !is AstrovisionUiState.Success) return

        val birthInput = currentState.response.birthInput

        viewModelScope.launch {
            _aiUiState.value = AiInterpretationUiState.Loading

            val request = AIInterpretationRequest(
                birthInput = birthInput,
                prompt = prompt,
                domain = domainCode
            )

            val result = repository.interpretEvidenceAi(request)
            result.fold(
                onSuccess = { response ->
                    _aiUiState.value = AiInterpretationUiState.Success(
                        domain = response.domain,
                        interpretation = response.interpretation,
                        validationStatus = response.validationStatus
                    )
                },
                onFailure = { error ->
                    _aiUiState.value = AiInterpretationUiState.Error(
                        error.localizedMessage ?: "AI interpretation service unavailable."
                    )
                }
            )
        }
    }

    fun resetForm() {
        nameState.value = ""
        yearState.value = 2000
        monthState.value = 1
        dayState.value = 1
        hourState.value = 12
        minuteState.value = 0
        selectedCityIndexState.value = 0
        timezoneStrState.value = PRESET_CITIES[0].tz
        placeNameState.value = PRESET_CITIES[0].name
        countryState.value = PRESET_CITIES[0].country
        latitudeState.value = PRESET_CITIES[0].lat
        longitudeState.value = PRESET_CITIES[0].lon

        _uiState.value = AstrovisionUiState.Idle
        _aiUiState.value = AiInterpretationUiState.Idle
        _activeTab.value = NavigationTab.FORM
    }
}
