package com.bluetrace.education.domain

data class KpiMetric(
    val title: String,
    val value: String,
    val trend: String
)

data class SafetyEvent(
    val time: String,
    val title: String,
    val detail: String
)
