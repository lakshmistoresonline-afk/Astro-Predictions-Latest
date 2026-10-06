package com.astro.predictions.ui.components

import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.astro.predictions.ui.theme.Champagne
import com.astro.predictions.ui.theme.DarkPurple
import com.astro.predictions.ui.theme.Ivory
import com.astro.predictions.ui.theme.MutedText
import com.astro.predictions.ui.viewmodel.AiInterpretationUiState

@Composable
fun AiInterpretationView(
    aiState: AiInterpretationUiState,
    onInterpretDomain: (String) -> Unit
) {
    var selectedDomain by remember { mutableStateOf("CAREER") }
    val domains = listOf(
        "CAREER", "FINANCE", "BUSINESS", "MARRIAGE", "RELATIONSHIP",
        "EDUCATION", "FAMILY", "CHILDREN", "PROPERTY", "TRAVEL",
        "RELOCATION", "SPIRITUALITY", "PERSONAL_DEVELOPMENT", "WELLBEING"
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("AI Evidence Interpretation", color = Champagne, fontSize = 20.sp, fontWeight = FontWeight.Bold)

        Card(
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.9f)),
            modifier = Modifier
                .fillMaxWidth()
                .border(1.dp, Champagne.copy(alpha = 0.3f), RoundedCornerShape(16.dp))
        ) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text("Select Domain to Synthesize", color = Champagne, fontSize = 14.sp, fontWeight = FontWeight.Bold)

                domains.chunked(2).forEach { rowDomains ->
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        rowDomains.forEach { dom ->
                            FilterChip(
                                selected = selectedDomain == dom,
                                onClick = { selectedDomain = dom },
                                label = { Text(dom, fontSize = 10.sp) },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }

                Button(
                    onClick = { onInterpretDomain(selectedDomain) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = Champagne)
                ) {
                    Text("Interpret Domain Evidence ($selectedDomain)", color = Color.Black, fontWeight = FontWeight.Bold)
                }
            }
        }

        when (aiState) {
            is AiInterpretationUiState.Loading -> {
                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.8f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(20.dp),
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        CircularProgressIndicator(color = Champagne, modifier = Modifier.size(24.dp))
                        Text("Synthesizing Parashari evidence via AI...", color = Ivory)
                    }
                }
            }
            is AiInterpretationUiState.Success -> {
                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = DarkPurple.copy(alpha = 0.9f)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text("Interpretation for ${aiState.domain}", color = Champagne, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text("Validation Status: ${aiState.validationStatus}", color = MutedText, fontSize = 10.sp)
                        Divider(color = Champagne.copy(alpha = 0.2f))
                        Text(aiState.interpretation, color = Ivory, fontSize = 13.sp, lineHeight = 20.sp)
                    }
                }
            }
            is AiInterpretationUiState.Error -> {
                Card(
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = Color(0x66990000)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(aiState.message, color = Color.White, modifier = Modifier.padding(16.dp))
                }
            }
            else -> {}
        }
    }
}
