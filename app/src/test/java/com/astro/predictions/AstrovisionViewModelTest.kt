package com.astro.predictions

import com.astro.predictions.data.model.PRESET_CITIES
import com.astro.predictions.ui.viewmodel.AstrovisionViewModel
import com.astro.predictions.ui.viewmodel.AstrovisionUiState
import com.astro.predictions.ui.viewmodel.NavigationTab
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test

class AstrovisionViewModelTest {

    private lateinit var viewModel: AstrovisionViewModel

    @Before
    fun setUp() {
        viewModel = AstrovisionViewModel()
    }

    @Test
    fun testInitialUiStateIsIdle() {
        assertEquals(AstrovisionUiState.Idle, viewModel.uiState.value)
        assertEquals(NavigationTab.FORM, viewModel.activeTab.value)
    }

    @Test
    fun testCleanFormInitialization() {
        assertEquals("", viewModel.nameState.value)
        assertEquals(2000, viewModel.yearState.value)
        assertEquals(1, viewModel.monthState.value)
        assertEquals(1, viewModel.dayState.value)
        assertEquals(12, viewModel.hourState.value)
        assertEquals(0, viewModel.minuteState.value)
    }

    @Test
    fun testCitySelectionUpdatesFormFields() {
        viewModel.onCitySelected(3) // London
        assertEquals("London", viewModel.placeNameState.value)
        assertEquals("United Kingdom", viewModel.countryState.value)
        assertEquals("Europe/London", viewModel.timezoneStrState.value)
    }

    @Test
    fun testEmptyNameProducesError() {
        viewModel.nameState.value = ""
        viewModel.calculateBirthProfile()
        assertTrue(viewModel.uiState.value is AstrovisionUiState.Error)
    }
}
