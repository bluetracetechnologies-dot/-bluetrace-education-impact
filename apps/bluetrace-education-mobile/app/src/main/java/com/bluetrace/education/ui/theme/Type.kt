package com.bluetrace.education.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

private val DisplayFamily = FontFamily.Serif
private val BodyFamily = FontFamily.SansSerif

val Typography = Typography(
	displaySmall = TextStyle(
		fontFamily = DisplayFamily,
		fontWeight = FontWeight.SemiBold,
		fontSize = 34.sp,
		lineHeight = 40.sp,
		letterSpacing = (-0.3).sp
	),
	headlineMedium = TextStyle(
		fontFamily = DisplayFamily,
		fontWeight = FontWeight.SemiBold,
		fontSize = 28.sp,
		lineHeight = 34.sp
	),
	titleLarge = TextStyle(
		fontFamily = BodyFamily,
		fontWeight = FontWeight.SemiBold,
		fontSize = 22.sp,
		lineHeight = 28.sp
	),
	titleMedium = TextStyle(
		fontFamily = BodyFamily,
		fontWeight = FontWeight.SemiBold,
		fontSize = 18.sp,
		lineHeight = 24.sp
	),
	titleSmall = TextStyle(
		fontFamily = BodyFamily,
		fontWeight = FontWeight.Medium,
		fontSize = 15.sp,
		lineHeight = 20.sp
	),
	bodyLarge = TextStyle(
		fontFamily = BodyFamily,
		fontWeight = FontWeight.Normal,
		fontSize = 16.sp,
		lineHeight = 23.sp
	),
	bodyMedium = TextStyle(
		fontFamily = BodyFamily,
		fontWeight = FontWeight.Normal,
		fontSize = 14.sp,
		lineHeight = 20.sp
	),
	bodySmall = TextStyle(
		fontFamily = BodyFamily,
		fontWeight = FontWeight.Normal,
		fontSize = 12.sp,
		lineHeight = 18.sp
	),
	labelLarge = TextStyle(
		fontFamily = BodyFamily,
		fontWeight = FontWeight.SemiBold,
		fontSize = 13.sp,
		lineHeight = 16.sp
	)
)
