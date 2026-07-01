package com.bluetrace.education.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.bluetrace.education.data.MockRepository

@Composable
fun BluetraceApp() {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Bluetrace Education MVP") })
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .background(Color(0xFFF5F8FA)),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Text(
                    text = "Management KPI Snapshot",
                    style = MaterialTheme.typography.titleMedium
                )
            }

            items(MockRepository.kpis) { metric ->
                KpiCard(title = metric.title, value = metric.value, trend = metric.trend)
            }

            item {
                Text(
                    text = "Student Safety Timeline",
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.padding(top = 8.dp)
                )
            }

            items(MockRepository.safetyTimeline) { event ->
                EventCard(time = event.time, title = event.title, detail = event.detail)
            }
        }
    }
}

@Composable
private fun KpiCard(title: String, value: String, trend: String) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(text = title, style = MaterialTheme.typography.titleSmall)
            Text(text = value, style = MaterialTheme.typography.headlineSmall, color = Color(0xFF14324A))
            Text(text = trend, style = MaterialTheme.typography.bodySmall, color = Color(0xFF1F8A70))
        }
    }
}

@Composable
private fun EventCard(time: String, title: String, detail: String) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            Text(text = time, style = MaterialTheme.typography.labelLarge, color = Color(0xFFC58F2B))
            Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(text = title, style = MaterialTheme.typography.titleSmall)
                Text(text = detail, style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}
