package com.bluetrace.education.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColors = lightColorScheme(
    primary = Navy700,
    onPrimary = SurfaceCard,
    secondary = Teal600,
    onSecondary = SurfaceCard,
    tertiary = Amber500,
    onTertiary = SurfaceCard,
    background = SurfaceSoft,
    onBackground = Ink900,
    surface = SurfaceCard,
    onSurface = Ink900,
    surfaceVariant = SurfaceTinted,
    onSurfaceVariant = Slate600,
    outline = BorderSoft
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF8CB8D2),
    onPrimary = Color(0xFF082134),
    secondary = Color(0xFF6ED0B6),
    onSecondary = Color(0xFF003A2E),
    tertiary = Color(0xFFEAC177),
    onTertiary = Color(0xFF4C3100),
    background = Color(0xFF101920),
    onBackground = Color(0xFFDFE8EE),
    surface = Color(0xFF14222C),
    onSurface = Color(0xFFE1EAF1),
    surfaceVariant = Color(0xFF233643),
    onSurfaceVariant = Color(0xFFB8C7D2),
    outline = Color(0xFF4A6170)
)

@Composable
fun BluetraceTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        typography = Typography,
        content = content
    )
}
