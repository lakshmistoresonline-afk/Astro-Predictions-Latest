package com.astro.predictions.data.repository

import com.astro.predictions.BuildConfig
import com.astro.predictions.data.api.AstrovisionApiService
import com.astro.predictions.data.api.AstrovisionNetworkException
import com.astro.predictions.data.api.NetworkModule
import com.astro.predictions.data.model.*
import retrofit2.HttpException
import java.io.IOException

class AstrovisionRepository(
    private val apiService: AstrovisionApiService = NetworkModule.createApiService(BuildConfig.BASE_URL)
) {

    fun setAuthToken(token: String?) {
        NetworkModule.setAuthToken(token)
    }

    private fun handleNetworkException(e: Exception): Throwable {
        return when (e) {
            is HttpException -> {
                val code = e.code()
                val message = when (code) {
                    400 -> "Invalid birth parameters or calculation input."
                    401 -> "Authentication required. Please log in."
                    403 -> "Access forbidden: insufficient permissions."
                    404 -> "Requested birth profile or report not found."
                    422 -> "Unprocessable calculation entity."
                    429 -> "Usage quota exceeded. Please try again later."
                    500 -> "Internal calculation engine error."
                    503 -> "NASA JPL DE440s ephemeris service temporarily unavailable."
                    else -> "Server error ($code)."
                }
                AstrovisionNetworkException(message, errorCode = "HTTP_$code", httpStatusCode = code)
            }
            is IOException -> {
                AstrovisionNetworkException(
                    "Network connection failed. Please check internet connection.",
                    errorCode = "CONNECTIVITY_OFFLINE",
                    httpStatusCode = 0
                )
            }
            else -> {
                AstrovisionNetworkException(
                    e.localizedMessage ?: "Unexpected network error.",
                    errorCode = "UNKNOWN_ERROR",
                    httpStatusCode = 0
                )
            }
        }
    }

    suspend fun calculateBirthProfile(request: BirthProfileRequest): Result<BirthProfileResponse> {
        return try {
            val response = apiService.calculateBirthProfile(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(handleNetworkException(e))
        }
    }

    suspend fun interpretEvidenceAi(request: AIInterpretationRequest): Result<AIInterpretationResponse> {
        return try {
            val response = apiService.interpretEvidenceAi(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(handleNetworkException(e))
        }
    }

    suspend fun getPanchanga(request: TransitRequest): Result<PanchangaResult> {
        return try {
            val response = apiService.getPanchanga(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(handleNetworkException(e))
        }
    }

    suspend fun getMuhurtaSuite(request: TransitRequest): Result<MuhurtaSuiteResult> {
        return try {
            val response = apiService.getMuhurtaSuite(request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(handleNetworkException(e))
        }
    }
}
