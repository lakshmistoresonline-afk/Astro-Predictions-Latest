package com.astro.predictions.data.api

class AstrovisionNetworkException(
    override val message: String,
    val errorCode: String = "NETWORK_ERROR",
    val httpStatusCode: Int = 0
) : Exception(message)
