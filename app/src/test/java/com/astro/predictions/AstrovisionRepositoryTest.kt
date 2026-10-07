package com.astro.predictions

import com.astro.predictions.data.api.AstrovisionApiService
import com.astro.predictions.data.api.AstrovisionNetworkException
import com.astro.predictions.data.model.*
import com.astro.predictions.data.repository.AstrovisionRepository
import kotlinx.coroutines.runBlocking
import okhttp3.ResponseBody.Companion.toResponseBody
import org.junit.Assert.*
import org.junit.Test
import retrofit2.HttpException
import retrofit2.Response
import java.io.IOException

class FakeAstrovisionApiService(
    private val shouldFailHttp: Int? = null,
    private val shouldThrowIoException: Boolean = false
) : AstrovisionApiService {

    override suspend fun calculateBirthProfile(request: BirthProfileRequest): BirthProfileResponse {
        if (shouldThrowIoException) {
            throw IOException("Network offline")
        }
        if (shouldFailHttp != null) {
            throw HttpException(Response.error<BirthProfileResponse>(shouldFailHttp, "".toResponseBody(null)))
        }

        val dummyChart = CanonicalVedicChart(
            inputData = request,
            timeNormalization = TimeNormalization("2020-01-01T12:00:00", "Asia/Kolkata", "2020-01-01T06:30:00Z", 5.5, 2458849.7, 2458849.7008, "UTC/TT"),
            ayanamshaMode = "Lahiri",
            ayanamshaValueDeg = 24.1,
            ascendant = RashiPosition(15.0, "Aries", 1, 15, 0, 0.0),
            mc = RashiPosition(285.0, "Capricorn", 10, 15, 0, 0.0),
            placements = emptyMap(),
            wholeSignHouses = emptyList(),
            calculationHash = "hash_chart"
        )

        val dummyEvidence = CanonicalAstrologyEvidence(
            birthInput = request,
            canonicalChart = dummyChart,
            vargaSuite = Full16VargaSuite("hash", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, emptyMap(), emptyList(), "hash"),
            vargaEvidence = null,
            natalDashaSuite = FullVimshottariDashaResult("2020-01-01T06:30:00Z", 45.0, BirthNakshatraInfo(1, "Ashwini", "Ketu", 1, 45.0, 0.5, 0.5), BirthDashaBalance("Ketu", 7.0, 3.5, 1278.0, "2020-01-01T06:30:00Z", "2023-07-01T06:30:00Z"), emptyList(), null, "hash"),
            activeDashaHierarchy = null,
            yogaSuite = YogaSuiteResult("hash", emptyList(), emptyList(), emptyMap(), "v1"),
            doshaSuite = DoshaSuiteResult("hash", emptyList(), emptyList(), emptyMap(), "v1"),
            shadbalaSuite = null,
            shadbalaEvidence = null,
            ashtakavargaSuite = null,
            ashtakavargaEvidence = null,
            jaiminiSuite = null,
            transitSnapshot = null,
            panchanga = null,
            muhurtaSuite = null,
            timingSuite = null,
            natalCalculationHash = "hash_natal",
            temporalCalculationHash = null,
            masterEvidenceHash = "master_hash_123"
        )

        return BirthProfileResponse(
            status = "success",
            birthInput = request,
            masterEvidence = dummyEvidence,
            predictions = ComprehensivePredictionPackage("master_hash_123", "v1", emptyMap(), null, "calc_hash"),
            svgChart = "<svg></svg>",
            report = null
        )
    }

    override suspend fun getPanchanga(request: TransitRequest): PanchangaResult = TODO()
    override suspend fun getMuhurtaSuite(request: TransitRequest): MuhurtaSuiteResult = TODO()
    override suspend fun getTransitSnapshot(request: TransitRequest): TransitSnapshot = TODO()
    override suspend fun getJaiminiSuite(request: BirthProfileRequest): JaiminiSuiteResult = TODO()
    override suspend fun interpretEvidenceAi(request: AIInterpretationRequest): AIInterpretationResponse = TODO()
    override suspend fun getAdminStats(): Map<String, Any> = TODO()
}

class AstrovisionRepositoryTest {

    @Test
    fun testCalculateBirthProfileSuccess() = runBlocking {
        val fakeService = FakeAstrovisionApiService()
        val repo = AstrovisionRepository(fakeService)

        val req = BirthProfileRequest(
            name = "Jane", year = 1995, month = 1, day = 1, hour = 12, minute = 0,
            timezoneStr = "Asia/Kolkata", latitude = 28.6139, longitude = 77.2090,
            placeName = "Delhi", country = "India"
        )

        val result = repo.calculateBirthProfile(req)
        assertTrue(result.isSuccess)
        val resp = result.getOrNull()
        assertNotNull(resp)
        assertEquals("success", resp?.status)
    }

    @Test
    fun testHttp401AuthenticationFailure() = runBlocking {
        val fakeService = FakeAstrovisionApiService(shouldFailHttp = 401)
        val repo = AstrovisionRepository(fakeService)

        val req = BirthProfileRequest(
            name = "Jane", year = 1995, month = 1, day = 1, hour = 12, minute = 0,
            timezoneStr = "Asia/Kolkata", latitude = 28.6139, longitude = 77.2090,
            placeName = "Delhi", country = "India"
        )

        val result = repo.calculateBirthProfile(req)
        assertTrue(result.isFailure)
        val exception = result.exceptionOrNull() as? AstrovisionNetworkException
        assertNotNull(exception)
        assertEquals(401, exception?.httpStatusCode)
        assertEquals("Authentication required. Please log in.", exception?.message)
    }

    @Test
    fun testHttp500ServerError() = runBlocking {
        val fakeService = FakeAstrovisionApiService(shouldFailHttp = 500)
        val repo = AstrovisionRepository(fakeService)

        val req = BirthProfileRequest(
            name = "Jane", year = 1995, month = 1, day = 1, hour = 12, minute = 0,
            timezoneStr = "Asia/Kolkata", latitude = 28.6139, longitude = 77.2090,
            placeName = "Delhi", country = "India"
        )

        val result = repo.calculateBirthProfile(req)
        assertTrue(result.isFailure)
        val exception = result.exceptionOrNull() as? AstrovisionNetworkException
        assertEquals(500, exception?.httpStatusCode)
    }

    @Test
    fun testOfflineNetworkIOException() = runBlocking {
        val fakeService = FakeAstrovisionApiService(shouldThrowIoException = true)
        val repo = AstrovisionRepository(fakeService)

        val req = BirthProfileRequest(
            name = "Jane", year = 1995, month = 1, day = 1, hour = 12, minute = 0,
            timezoneStr = "Asia/Kolkata", latitude = 28.6139, longitude = 77.2090,
            placeName = "Delhi", country = "India"
        )

        val result = repo.calculateBirthProfile(req)
        assertTrue(result.isFailure)
        val exception = result.exceptionOrNull() as? AstrovisionNetworkException
        assertEquals("CONNECTIVITY_OFFLINE", exception?.errorCode)
    }
}
