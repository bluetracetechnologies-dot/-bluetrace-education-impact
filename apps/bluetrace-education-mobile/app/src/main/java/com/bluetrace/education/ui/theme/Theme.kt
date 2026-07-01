package com.bluetrace.education.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColors = lightColorScheme(
    primary = Color(0xFF14324A),
    secondary = Color(0xFF1F8A70),
    tertiary = Color(0xFFC58F2B)
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF7CA9C5),
    secondary = Color(0xFF5AB89E),
    tertiary = Color(0xFFE1B15C)
)

@Composable
fun BluetraceTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColors,
        typography = Typography,
        content = content
    )
}
