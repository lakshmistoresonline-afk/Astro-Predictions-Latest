package com.astro.predictions.data.api

import com.astro.predictions.data.model.*
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface AstrovisionApiService {

    @POST("api/v1/birth-profile")
    suspend fun calculateBirthProfile(
        @Body request: BirthProfileRequest
    ): BirthProfileResponse

    @POST("api/v1/panchanga")
    suspend fun getPanchanga(
        @Body request: TransitRequest
    ): PanchangaResult

    @POST("api/v1/muhurta")
    suspend fun getMuhurtaSuite(
        @Body request: TransitRequest
    ): MuhurtaSuiteResult

    @POST("api/v1/transits")
    suspend fun getTransitSnapshot(
        @Body request: TransitRequest
    ): TransitSnapshot

    @POST("api/v1/jaimini")
    suspend fun getJaiminiSuite(
        @Body request: BirthProfileRequest
    ): JaiminiSuiteResult

    @POST("api/v1/interpret-evidence")
    suspend fun interpretEvidenceAi(
        @Body request: AIInterpretationRequest
    ): AIInterpretationResponse

    @GET("api/v1/admin/stats")
    suspend fun getAdminStats(): Map<String, Any>
}
