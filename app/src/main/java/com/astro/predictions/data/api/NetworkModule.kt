package com.astro.predictions.data.api

import com.astro.predictions.BuildConfig
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.UUID
import java.util.concurrent.TimeUnit

object NetworkModule {

    private var currentAuthToken: String? = null

    fun setAuthToken(token: String?) {
        currentAuthToken = token
    }

    fun createApiService(baseUrl: String = BuildConfig.BASE_URL): AstrovisionApiService {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            // Disable BODY logging in release builds to avoid exposing personal birth data in logs
            level = if (BuildConfig.DEBUG) {
                HttpLoggingInterceptor.Level.BASIC
            } else {
                HttpLoggingInterceptor.Level.NONE
            }
        }

        val authAndCorrelationInterceptor = Interceptor { chain ->
            val original = chain.request()
            val requestBuilder = original.newBuilder()

            // Attach Bearer token if present
            currentAuthToken?.let { token ->
                requestBuilder.header("Authorization", "Bearer $token")
            }

            // Attach or preserve X-Request-ID correlation ID
            val reqId = original.header("X-Request-ID") ?: "req_${UUID.randomUUID().toString().take(12)}"
            requestBuilder.header("X-Request-ID", reqId)

            chain.proceed(requestBuilder.build())
        }

        val okHttpClient = OkHttpClient.Builder()
            .addInterceptor(authAndCorrelationInterceptor)
            .addInterceptor(loggingInterceptor)
            .connectTimeout(20, TimeUnit.SECONDS)
            .readTimeout(20, TimeUnit.SECONDS)
            .writeTimeout(20, TimeUnit.SECONDS)
            .build()

        val retrofit = Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        return retrofit.create(AstrovisionApiService::class.java)
    }
}
