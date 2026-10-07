package com.astro.predictions

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.astro.predictions.data.model.*
import com.astro.predictions.ui.components.*
import com.astro.predictions.ui.theme.*
import com.astro.predictions.ui.viewmodel.*

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AstroPredictionsTheme {
                AstrovisionApp()
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AstrovisionApp(
    viewModel: AstrovisionViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    val aiState by viewModel.aiUiState.collectAsState()
    val activeTab by viewModel.activeTab.collectAsState()

    val name by viewModel.nameState.collectAsState()
    val year by viewModel.yearState.collectAsState()
    val month by viewModel.monthState.collectAsState()
    val day by viewModel.dayState.collectAsState()
    val hour by viewModel.hourState.collectAsState()
    val minute by viewModel.minuteState.collectAsState()
    val selectedCityIndex by viewModel.selectedCityIndexState.collectAsState()
    val timezoneStr by viewModel.timezoneStrState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("✦ Astrovision", color = Champagne, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                        Text("NASA JPL DE440s Ephemeris", color = MutedText, fontSize = 10.sp)
                    }
                },
                actions = {
                    if (uiState is AstrovisionUiState.Success) {
                        TextButton(onClick = { viewModel.resetForm() }) {
                            Text("New Profile", color = Champagne)
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Midnight)
            )
        },
        bottomBar = {
            if (uiState is AstrovisionUiState.Success) {
                ScrollableTabRow(
                    selectedTabIndex = activeTab.ordinal,
                    containerColor = Midnight,
                    contentColor = Champagne,
                    edgePadding = 8.dp
                ) {
                    NavigationTab.values().filter { it != NavigationTab.FORM }.forEach { tab ->
                        Tab(
                            selected = activeTab == tab,
                            onClick = { viewModel.selectTab(tab) },
                            text = { Text(tab.label, fontSize = 11.sp, fontWeight = if (activeTab == tab) FontWeight.Bold else FontWeight.Normal) }
                        )
                    }
                }
            }
        },
        containerColor = Midnight
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when (val state = uiState) {
                is AstrovisionUiState.Idle -> {
                    BirthProfileFormScreen(
                        name = name,
                        onNameChange = { viewModel.nameState.value = it },
                        year = year,
                        onYearChange = { viewModel.yearState.value = it },
                        month = month,
                        onMonthChange = { viewModel.monthState.value = it },
                        day = day,
                        onDayChange = { viewModel.dayState.value = it },
                        hour = hour,
                        onHourChange = { viewModel.hourState.value = it },
                        minute = minute,
                        onMinuteChange = { viewModel.minuteState.value = it },
                        selectedCityIndex = selectedCityIndex,
                        onCitySelected = { viewModel.onCitySelected(it) },
                        timezoneStr = timezoneStr,
                        onTimezoneChange = { viewModel.timezoneStrState.value = it },
                        onSubmit = { viewModel.calculateBirthProfile() }
                    )
                }
                is AstrovisionUiState.Loading -> {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(Midnight.copy(alpha = 0.95f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.spacedBy(16.dp)
                        ) {
                            CircularProgressIndicator(color = Champagne, modifier = Modifier.size(48.dp))
                            Text(state.message, color = Ivory, fontSize = 14.sp)
                        }
                    }
                }
                is AstrovisionUiState.Error -> {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text("Calculation Error", color = Color.Red, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(state.message, color = Ivory, fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(24.dp))
                        Button(
                            onClick = { viewModel.resetForm() },
                            colors = ButtonDefaults.buttonColors(containerColor = Champagne)
                        ) {
                            Text("Back to Birth Profile Entry", color = Midnight)
                        }
                    }
                }
                is AstrovisionUiState.Success -> {
                    val resp = state.response
                    val chart = resp.masterEvidence.canonicalChart

                    when (activeTab) {
                        NavigationTab.DASHBOARD -> DashboardOverview(resp)
                        NavigationTab.KUNDALI -> KundaliChartView(resp.svgChart)
                        NavigationTab.PLANETS -> PlanetaryPositionsView(chart)
                        NavigationTab.VARGAS -> VargasView(resp.masterEvidence.vargaSuite)
                        NavigationTab.DASHAS -> DashasView(resp.masterEvidence.natalDashaSuite)
                        NavigationTab.YOGAS_DOSHAS -> YogasDoshasView(resp.masterEvidence.yogaSuite, resp.masterEvidence.doshaSuite)
                        NavigationTab.STRENGTH -> ShadbalaAshtakavargaView(
                            shadbalaSuite = resp.masterEvidence.shadbalaSuite,
                            ashtakavargaEvidence = resp.masterEvidence.ashtakavargaEvidence
                        )
                        NavigationTab.JAIMINI -> JaiminiView(
                            jaiminiSuite = resp.masterEvidence.jaiminiSuite
                        )
                        NavigationTab.PANCHANGA -> PanchangaMuhurtaView(resp.masterEvidence.panchanga, resp.masterEvidence.muhurtaSuite)
                        NavigationTab.PREDICTIONS -> PredictionsView(resp.predictions)
                        NavigationTab.AI_INTERPRETATION -> AiInterpretationView(
                            aiState = aiState,
                            onInterpretDomain = { dom -> viewModel.interpretDomainAi(dom) }
                        )
                        else -> DashboardOverview(resp)
                    }
                }
            }
        }
    }
}
