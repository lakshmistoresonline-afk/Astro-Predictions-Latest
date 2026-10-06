package com.astro.predictions

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class AstrovisionAppInstrumentedTest {

    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun testAppLaunchesWithBirthParticularsForm() {
        composeTestRule.onNodeWithText("Enter Birth Particulars").assertExists()
        composeTestRule.onNodeWithText("Calculate Birth Chart").assertExists()
    }
}
