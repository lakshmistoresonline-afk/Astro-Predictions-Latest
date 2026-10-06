package com.astro.predictions.ui.components

import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import com.astro.predictions.data.model.*
import com.astro.predictions.ui.theme.*

// --- Birth Profile Form Screen ---
@Composable
fun BirthProfileFormScreen(
    name: String,
    onNameChange: (String) -> Unit,
    year: Int,
    onYearChange: (Int) -> Unit,
    month: Int,
    onMonthChange: (Int) -> Unit,
    day: Int,
    onDayChange: (Int) -> Unit,
    hour: Int,
    onHourChange: (Int) -> Unit,
    minute: Int,
    onMinuteChange: (Int) -> Unit,
    selectedCityIndex: Int,
    onCitySelected: (Int) -> Unit,
    timezoneStr: String,
    onTimezoneChange: (String) -> Unit,
    onSubmit: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Card(
            shape = RoundedCornerShape(24.dp),
            colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.9f)),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Champagne.copy(alpha = 0.4f), RoundedCornerShape(24.dp))
        ) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Text(
                    text = "Enter Birth Particulars",
                    style = MaterialTheme.typography.titleLarge,
                    color = Champagne,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "Calculated using NASA JPL DE440s Ephemeris Kernel & 100% Deterministic Parashari Engines.",
                    style = MaterialTheme.typography.bodySmall,
                    color = Ivory.copy(alpha = 0.7f)
                )

                OutlinedTextField(
                    value = name,
                    onValueChange = onNameChange,
                    label = { Text("Full Birth Name", color = MutedText) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Champagne,
                        unfocusedBorderColor = Champagne.copy(alpha = 0.4f),
                        focusedTextColor = Ivory,
                        unfocusedTextColor = Ivory
                    )
                )

                // Date Fields
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    OutlinedTextField(
                        value = year.toString(),
                        onValueChange = { it.toIntOrNull()?.let(onYearChange) },
                        label = { Text("Year", color = MutedText) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Champagne, focusedTextColor = Ivory, unfocusedTextColor = Ivory)
                    )
                    OutlinedTextField(
                        value = month.toString(),
                        onValueChange = { it.toIntOrNull()?.let(onMonthChange) },
                        label = { Text("Month", color = MutedText) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Champagne, focusedTextColor = Ivory, unfocusedTextColor = Ivory)
                    )
                    OutlinedTextField(
                        value = day.toString(),
                        onValueChange = { it.toIntOrNull()?.let(onDayChange) },
                        label = { Text("Day", color = MutedText) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Champagne, focusedTextColor = Ivory, unfocusedTextColor = Ivory)
                    )
                }

                // Time Fields
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    OutlinedTextField(
                        value = hour.toString(),
                        onValueChange = { it.toIntOrNull()?.let(onHourChange) },
                        label = { Text("Hour (0-23)", color = MutedText) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Champagne, focusedTextColor = Ivory, unfocusedTextColor = Ivory)
                    )
                    OutlinedTextField(
                        value = minute.toString(),
                        onValueChange = { it.toIntOrNull()?.let(onMinuteChange) },
                        label = { Text("Minute (0-59)", color = MutedText) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.weight(1f),
                        colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Champagne, focusedTextColor = Ivory, unfocusedTextColor = Ivory)
                    )
                }

                // City Dropdown Selector
                Text("Select Birth Location", style = MaterialTheme.typography.labelMedium, color = MutedText)
                PRESET_CITIES.forEachIndexed { idx, city ->
                    FilterChip(
                        selected = selectedCityIndex == idx,
                        onClick = { onCitySelected(idx) },
                        label = { Text("${city.name}, ${city.country} (${city.tz})") },
                        modifier = Modifier.fillMaxWidth(),
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = Champagne.copy(alpha = 0.3f),
                            selectedLabelColor = Champagne
                        )
                    )
                }

                OutlinedTextField(
                    value = timezoneStr,
                    onValueChange = onTimezoneChange,
                    label = { Text("IANA Timezone Key", color = MutedText) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = OutlinedTextFieldDefaults.colors(focusedBorderColor = Champagne, focusedTextColor = Ivory, unfocusedTextColor = Ivory)
                )

                Button(
                    onClick = onSubmit,
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(54.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Champagne, contentColor = Midnight)
                ) {
                    Text("Calculate Birth Chart", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
            }
        }
    }
}

// --- Dashboard Overview ---
@Composable
fun DashboardOverview(response: BirthProfileResponse) {
    val report = response.report
    val masterEv = response.masterEvidence
    val chart = masterEv.canonicalChart

    val ascSign = chart.ascendant.sign
    val ascDegree = "${chart.ascendant.degree}°"
    val moonPlacement = chart.placements["Moon"]
    val sunPlacement = chart.placements["Sun"]

    val moonSign = moonPlacement?.rashi?.sign ?: "Unavailable"
    val sunSign = sunPlacement?.rashi?.sign ?: "Unavailable"
    val moonNakshatra = moonPlacement?.nakshatraPada?.nakshatra ?: "Unavailable"
    val moonPada = moonPlacement?.nakshatraPada?.pada?.toString() ?: ""

    val activeDasha = response.predictions.activeDashaSummary ?: "Unavailable"

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = DarkPurple),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("✦ Cosmic Profile", color = Champagne, fontSize = 12.sp, fontWeight = FontWeight.ExtraBold)
                Text(response.birthInput.name, color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
                Text(
                    "Born ${response.birthInput.year}-${response.birthInput.month}-${response.birthInput.day} at ${response.birthInput.hour}:${response.birthInput.minute} (${response.birthInput.timezoneStr})",
                    color = MutedText, fontSize = 12.sp
                )
            }
        }

        // Summary Cards
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            SummaryCard("Ascendant (Lagna)", "$ascSign $ascDegree", Modifier.weight(1f))
            SummaryCard("Moon Sign (Rashi)", moonSign, Modifier.weight(1f))
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            SummaryCard("Sun Sign", sunSign, Modifier.weight(1f))
            SummaryCard("Nakshatra & Pada", "$moonNakshatra ${if (moonPada.isNotEmpty()) "P$moonPada" else ""}", Modifier.weight(1f))
        }

        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("Active Vimshottari Dasha", color = Champagne, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                Text(activeDasha, color = Color.White, fontSize = 14.sp)
            }
        }
    }
}

@Composable
fun SummaryCard(title: String, value: String, modifier: Modifier = Modifier) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
        modifier = modifier
    ) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(title, color = Champagne, fontSize = 10.sp, fontWeight = FontWeight.Bold)
            Text(value, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
    }
}

// --- Kundali SVG View ---
@Composable
fun KundaliChartView(svgHtml: String?) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        if (svgHtml != null) {
            AndroidView(
                factory = { context ->
                    WebView(context).apply {
                        webViewClient = WebViewClient()
                        settings.javaScriptEnabled = true
                        loadDataWithBaseURL(null, "<html style='background:#050816;display:flex;justify-content:center;align-items:center;height:100%'><body style='margin:0;padding:0'>$svgHtml</body></html>", "text/html", "UTF-8", null)
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(380.dp)
            )
        } else {
            Text("Kundali Chart SVG Unavailable", color = MutedText)
        }
    }
}

// --- Planetary Positions Table ---
@Composable
fun PlanetaryPositionsView(chart: CanonicalVedicChart) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            Text("Planetary Placements", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
        items(chart.placements.values.toList()) { p ->
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(p.bodyName, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text("${p.rashi.sign} (${p.rashi.degree}°) | ${p.nakshatraPada.nakshatra} P${p.nakshatraPada.pada}", color = MutedText, fontSize = 12.sp)
                    }
                    Text(
                        if (p.retrograde) "RETROGRADE" else "DIRECT",
                        color = if (p.retrograde) Color.Red else Color.Green,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}

// --- 16 Vargas Grid ---
@Composable
fun VargasView(vargaSuite: Full16VargaSuite) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            Text("16 Parashari Divisional Charts", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
        items(vargaSuite.vargas.values.toList()) { v ->
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text("${v.division} - ${v.divisionName}", color = Champagne, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    Text("Ascendant: ${v.ascendant.vargaSign}", color = Color.White, fontSize = 12.sp)
                    Text("Sun: ${v.placements["Sun"]?.vargaSign ?: "N/A"} | Moon: ${v.placements["Moon"]?.vargaSign ?: "N/A"}", color = MutedText, fontSize = 10.sp)
                }
            }
        }
    }
}

// --- Vimshottari Dashas View ---
@Composable
fun DashasView(dashaSuite: FullVimshottariDashaResult) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            Text("Vimshottari Dasha Timeline", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Text("Birth Balance: ${dashaSuite.birthBalance.mahadashaLord} (${dashaSuite.birthBalance.remainingYears} Years Remaining)", color = MutedText, fontSize = 12.sp)
        }
        items(dashaSuite.mahadashas) { md ->
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text("Mahadasha: ${md.lord}", color = Champagne, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                    Text("${md.startUtcIso.take(10)} to ${md.endUtcIso.take(10)} (${md.durationYears} Years)", color = MutedText, fontSize = 12.sp)
                }
            }
        }
    }
}

// --- Yogas & Doshas View ---
@Composable
fun YogasDoshasView(yogaSuite: YogaSuiteResult, doshaSuite: DoshaSuiteResult) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Text("Detected Yogas (${yogaSuite.detectedYogas.size})", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
        items(yogaSuite.detectedYogas) { y ->
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(y.name, color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    Text("Category: ${y.category} | Status: ${y.status}", color = MutedText, fontSize = 10.sp)
                }
            }
        }

        item {
            Spacer(modifier = Modifier.height(8.dp))
            Text("Detected Doshas (${doshaSuite.detectedDoshas.size})", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
        items(doshaSuite.detectedDoshas) { d ->
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(d.name, color = Color.White, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    Text("Status: ${d.status}", color = MutedText, fontSize = 10.sp)
                }
            }
        }
    }
}

// --- Panchanga & Muhurta View ---
@Composable
fun PanchangaMuhurtaView(panchanga: PanchangaResult?, muhurtaSuite: MuhurtaSuiteResult?) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Panchanga & Muhurta", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)

        if (panchanga != null) {
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("Tithi: ${panchanga.tithi.tithiName} (${panchanga.tithi.paksha})", color = Color.White)
                    Text("Vara: ${panchanga.vara.dayNameEnglish} (${panchanga.vara.dayNameSanskrit})", color = Color.White)
                    Text("Nakshatra: ${panchanga.nakshatraName} (Pada ${panchanga.nakshatraPada})", color = Color.White)
                    Text("Nitya Yoga: ${panchanga.nityaYoga.yogaName}", color = Color.White)
                    Text("Karana: ${panchanga.karana.karanaName}", color = Color.White)
                }
            }
        } else {
            Text("Panchanga Evidence Unavailable", color = MutedText)
        }

        if (muhurtaSuite != null) {
            Text("Activity Muhurtas", color = Champagne, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            muhurtaSuite.evaluations.forEach { (act, eval) ->
                Card(
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text("$act: ${eval.recommendation}", color = Color.White, fontWeight = FontWeight.Bold)
                        Text(eval.summary, color = MutedText, fontSize = 10.sp)
                    }
                }
            }
        }
    }
}

// --- Predictions View ---
@Composable
fun PredictionsView(predictions: ComprehensivePredictionPackage) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        item {
            Text("14 Domain Predictions Evidence", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
        items(predictions.domainPredictions.entries.toList()) { (dom, data) ->
            Card(
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(data.ruleDefinition.domainTitle, color = Champagne, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    Text("Status: ${data.evidenceStatus} | Class: ${data.evidenceStrengthClass ?: "N/A"}", color = Color.White, fontSize = 12.sp)
                    Text(data.ruleDefinition.ruleDescription, color = MutedText, fontSize = 10.sp)
                }
            }
        }
    }
}
