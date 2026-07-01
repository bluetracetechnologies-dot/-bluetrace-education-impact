package com.bluetrace.education.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.bluetrace.education.data.MockRepository
import com.bluetrace.education.domain.KpiMetric
import com.bluetrace.education.ui.theme.Amber500
import com.bluetrace.education.ui.theme.BorderSoft
import com.bluetrace.education.ui.theme.HeroEnd
import com.bluetrace.education.ui.theme.HeroStart
import com.bluetrace.education.ui.theme.Ink700
import com.bluetrace.education.ui.theme.Navy700
import com.bluetrace.education.ui.theme.Slate400
import com.bluetrace.education.ui.theme.SuccessSoft
import com.bluetrace.education.ui.theme.SurfaceCard
import com.bluetrace.education.ui.theme.SurfaceSoft
import com.bluetrace.education.ui.theme.Teal600

private enum class UserRole { Parent, Teacher, Principal }

private enum class ScreenState { Live, Loading, Empty, Error }

@Composable
fun BluetraceApp() {
    var selectedTab by rememberSaveable { mutableIntStateOf(0) }
    var selectedRole by rememberSaveable { mutableStateOf(UserRole.Principal) }
    var screenState by rememberSaveable { mutableStateOf(ScreenState.Live) }
    val tabs = listOf("Command", "Safety", "Profile")

    Scaffold(
        containerColor = SurfaceSoft,
        bottomBar = {
            NavigationBar(containerColor = SurfaceCard) {
                tabs.forEachIndexed { index, title ->
                    NavigationBarItem(
                        selected = selectedTab == index,
                        onClick = { selectedTab = index },
                        icon = {
                            Box(
                                modifier = Modifier
                                    .size(10.dp)
                                    .clip(CircleShape)
                                    .background(if (selectedTab == index) Teal600 else Slate400)
                            )
                        },
                        label = { Text(title) }
                    )
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item { HeroPanel() }
            item {
                RoleSwitcher(
                    selectedRole = selectedRole,
                    onRoleSelect = { selectedRole = it }
                )
            }
            item {
                StateSwitcher(
                    screenState = screenState,
                    onStateSelect = { screenState = it }
                )
            }
            when (screenState) {
                ScreenState.Live -> {
                    if (selectedTab == 0) {
                        item {
                            SectionTitle(
                                title = when (selectedRole) {
                                    UserRole.Parent -> "Family command view"
                                    UserRole.Teacher -> "Teaching command view"
                                    UserRole.Principal -> "Institution command view"
                                },
                                subtitle = "Role-aware priorities with premium clarity"
                            )
                        }
                        item { RoleSpotlight(role = selectedRole) }
                        item {
                            SectionTitle(
                                title = "Today at a glance",
                                subtitle = "Live leadership metrics"
                            )
                        }
                        item { KpiGrid(metrics = MockRepository.kpis) }
                    } else if (selectedTab == 1) {
                        item {
                            SectionTitle(
                                title = "Student safety timeline",
                                subtitle = "Operational events and confirmations"
                            )
                        }
                        itemsIndexed(MockRepository.safetyTimeline) { index, event ->
                            EventCard(
                                time = event.time,
                                title = event.title,
                                detail = event.detail,
                                isLast = index == MockRepository.safetyTimeline.lastIndex
                            )
                        }
                    } else {
                        item {
                            SectionTitle(
                                title = "Profile and preferences",
                                subtitle = "Your role context and smart defaults"
                            )
                        }
                        item { ProfileCard(role = selectedRole) }
                    }
                }

                ScreenState.Loading -> {
                    item { LoadingCard() }
                }

                ScreenState.Empty -> {
                    item { EmptyCard(selectedTab = tabs[selectedTab]) }
                }

                ScreenState.Error -> {
                    item { ErrorCard() }
                }
            }
        }
    }
}

@Composable
private fun RoleSwitcher(selectedRole: UserRole, onRoleSelect: (UserRole) -> Unit) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = SurfaceCard,
        tonalElevation = 1.dp
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            UserRole.entries.forEach { role ->
                val selected = selectedRole == role
                Surface(
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(12.dp),
                    color = if (selected) Teal600 else SurfaceSoft,
                    onClick = { onRoleSelect(role) }
                ) {
                    Text(
                        text = role.name,
                        modifier = Modifier.padding(vertical = 10.dp),
                        color = if (selected) Color.White else Navy700,
                        style = MaterialTheme.typography.labelLarge,
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center
                    )
                }
            }
        }
    }
}

@Composable
private fun StateSwitcher(screenState: ScreenState, onStateSelect: (ScreenState) -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        ScreenState.entries.forEach { state ->
            val active = state == screenState
            Surface(
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(12.dp),
                color = if (active) Navy700 else SurfaceCard,
                border = BorderStroke(1.dp, BorderSoft),
                onClick = { onStateSelect(state) }
            ) {
                Text(
                    text = state.name,
                    modifier = Modifier.padding(vertical = 8.dp),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                    style = MaterialTheme.typography.bodySmall,
                    color = if (active) Color.White else Ink700
                )
            }
        }
    }
}

@Composable
private fun RoleSpotlight(role: UserRole) {
    val title = when (role) {
        UserRole.Parent -> "Parent confidence loop"
        UserRole.Teacher -> "Teacher productivity loop"
        UserRole.Principal -> "Principal governance loop"
    }
    val description = when (role) {
        UserRole.Parent -> "Real-time boarding, class updates, and pickup closure in one trusted stream."
        UserRole.Teacher -> "AI-assisted planning, differentiated delivery, and cleaner family communication."
        UserRole.Principal -> "Decision-ready KPIs with cross-team accountability and measurable outcomes."
    }

    Card(
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(text = title, style = MaterialTheme.typography.titleMedium, color = Navy700)
            Text(text = description, style = MaterialTheme.typography.bodyMedium, color = Ink700)
        }
    }
}

@Composable
private fun HeroPanel() {
    Card(
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = Color.Transparent)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(brush = Brush.linearGradient(listOf(HeroStart, HeroEnd)))
                .padding(20.dp)
        ) {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Surface(
                    shape = RoundedCornerShape(20.dp),
                    color = Color.White.copy(alpha = 0.16f)
                ) {
                    Text(
                        text = "PRESIDENCY COMMAND CENTER",
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                        style = MaterialTheme.typography.labelLarge,
                        color = Color.White
                    )
                }
                Text(
                    text = "Smart, calm, always accountable.",
                    style = MaterialTheme.typography.displaySmall,
                    color = Color.White
                )
                Text(
                    text = "Unified parent trust, teacher productivity, and transport governance.",
                    style = MaterialTheme.typography.bodyLarge,
                    color = Color.White.copy(alpha = 0.92f)
                )
            }
        }
    }
}

@Composable
private fun SectionTitle(title: String, subtitle: String) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Text(text = title, style = MaterialTheme.typography.titleLarge, color = Navy700)
        Text(text = subtitle, style = MaterialTheme.typography.bodySmall, color = Ink700)
    }
}

@Composable
private fun KpiGrid(metrics: List<KpiMetric>) {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        metrics.chunked(2).forEach { row ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                row.forEach { metric ->
                    KpiCard(
                        title = metric.title,
                        value = metric.value,
                        trend = metric.trend,
                        modifier = Modifier.weight(1f)
                    )
                }
                if (row.size == 1) {
                    Spacer(modifier = Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
private fun KpiCard(title: String, value: String, trend: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(text = title, style = MaterialTheme.typography.bodySmall, color = Ink700)
            Text(
                text = value,
                style = MaterialTheme.typography.headlineMedium,
                color = Navy700,
                fontWeight = FontWeight.SemiBold
            )
            Surface(
                shape = RoundedCornerShape(12.dp),
                color = SuccessSoft
            ) {
                Text(
                    text = trend,
                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 5.dp),
                    style = MaterialTheme.typography.labelLarge,
                    color = Teal600
                )
            }
        }
    }
}

@Composable
private fun EventCard(time: String, title: String, detail: String, isLast: Boolean) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
        modifier = Modifier.border(BorderStroke(1.dp, BorderSoft), RoundedCornerShape(16.dp))
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Box(
                    modifier = Modifier
                        .size(12.dp)
                        .clip(CircleShape)
                        .background(Amber500)
                )
                if (!isLast) {
                    Box(
                        modifier = Modifier
                            .padding(top = 4.dp)
                            .width(2.dp)
                            .height(30.dp)
                            .background(BorderSoft)
                    )
                }
            }

            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(text = title, style = MaterialTheme.typography.titleSmall, color = Navy700)
                    Text(text = time, style = MaterialTheme.typography.labelLarge, color = Amber500)
                }
                Text(text = detail, style = MaterialTheme.typography.bodyMedium, color = Ink700)
                HorizontalDivider(color = BorderSoft)
                Text(text = "Status: verified", style = MaterialTheme.typography.bodySmall, color = Teal600)
            }
        }
    }
}

@Composable
private fun ProfileCard(role: UserRole) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard)
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(text = "Active role", style = MaterialTheme.typography.bodySmall, color = Ink700)
            Text(text = role.name, style = MaterialTheme.typography.titleLarge, color = Navy700)
            HorizontalDivider(color = BorderSoft)
            Text(
                text = "Notifications, privacy, and alert routing are configured for this persona.",
                style = MaterialTheme.typography.bodyMedium,
                color = Ink700
            )
        }
    }
}

@Composable
private fun LoadingCard() {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            CircularProgressIndicator(color = Teal600)
            Text(text = "Syncing live school intelligence...", color = Ink700)
        }
    }
}

@Composable
private fun EmptyCard(selectedTab: String) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(text = "No data yet", style = MaterialTheme.typography.titleMedium, color = Navy700)
            Text(
                text = "No items found for $selectedTab right now. Once activity starts, cards will appear here.",
                style = MaterialTheme.typography.bodyMedium,
                color = Ink700
            )
        }
    }
}

@Composable
private fun ErrorCard() {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = SurfaceCard),
        border = BorderStroke(1.dp, Amber500.copy(alpha = 0.4f))
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(text = "Connection interrupted", style = MaterialTheme.typography.titleMedium, color = Navy700)
            Text(
                text = "We could not refresh data. Please retry from a stable network.",
                style = MaterialTheme.typography.bodyMedium,
                color = Ink700
            )
        }
    }
}
