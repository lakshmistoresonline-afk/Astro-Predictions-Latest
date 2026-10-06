package com.astro.predictions.data.repository

import com.astro.predictions.data.api.AstrovisionApiService
import com.astro.predictions.data.model.*
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

class AstrovisionRepository(
    baseUrl: String = "http://10.0.2.2:8000/" // Default Android Emulator host pointing to local FastAPI server
) {
    private val apiService: AstrovisionApiService

    init {
        val logging = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }

        val okHttpClient = OkHttpClient.Builder()
            .addInterceptor(logging)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()

        val retrofit = Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        apiService = retrofit.create(AstrovisionApiService::class.java)
    }

    suspend fun calculateBirthProfile(request: BirthProfileRequest): Result<BirthProfileResponse> {
        return try {
            val response = apiService.calculateBirthProfile(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun interpretEvidenceAi(request: AIInterpretationRequest): Result<AIInterpretationResponse> {
        return try {
            val response = apiService.interpretEvidenceAi(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getPanchanga(request: TransitRequest): Result<PanchangaResult> {
        return try {
            val response = apiService.getPanchanga(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getMuhurtaSuite(request: TransitRequest): Result<MuhurtaSuiteResult> {
        return try {
            val response = apiService.getMuhurtaSuite(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
