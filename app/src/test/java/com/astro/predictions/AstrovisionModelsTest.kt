package com.astro.predictions

import com.astro.predictions.data.model.BirthProfileRequest
import com.astro.predictions.data.model.PRESET_CITIES
import org.junit.Assert.*
import org.junit.Test

class AstrovisionModelsTest {

    @Test
    fun testPresetCitiesContainValidTimezones() {
        assertTrue(PRESET_CITIES.isNotEmpty())
        PRESET_CITIES.forEach { city ->
            assertNotNull(city.tz)
            assertTrue(city.tz.contains("/"))
        }
    }

    @Test
    fun testBirthProfileRequestInstantiation() {
        val req = BirthProfileRequest(
            name = "John Doe",
            year = 1990, month = 5, day = 15,
            hour = 14, minute = 30, second = 0,
            timezoneStr = "Asia/Kolkata",
            latitude = 18.9220, longitude = 72.8347,
            placeName = "Mumbai", country = "India"
        )

        assertEquals("John Doe", req.name)
        assertEquals(1990, req.year)
        assertEquals("Asia/Kolkata", req.timezoneStr)
    }
}
