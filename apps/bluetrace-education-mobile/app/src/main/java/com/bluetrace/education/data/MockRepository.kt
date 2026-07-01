package com.bluetrace.education.data

import com.bluetrace.education.domain.KpiMetric
import com.bluetrace.education.domain.SafetyEvent

object MockRepository {
    val kpis = listOf(
        KpiMetric("Boarding confirmation", "98%", "+2% vs last week"),
        KpiMetric("Teacher prep time saved", "34%", "+6% this month"),
        KpiMetric("Assignment completion", "91%", "+4% this term"),
        KpiMetric("Parent acknowledgement", "89%", "+3% this month")
    )

    val safetyTimeline = listOf(
        SafetyEvent("07:42", "Boarding confirmed", "Route A3 checkpoint tapped"),
        SafetyEvent("13:05", "Class circular delivered", "Homework + notice synced"),
        SafetyEvent("16:18", "Pickup confirmed", "Guardian acknowledgement received")
    )
}
