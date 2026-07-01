package com.bluetrace.education

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.bluetrace.education.ui.BluetraceApp
import com.bluetrace.education.ui.theme.BluetraceTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            BluetraceTheme {
                BluetraceApp()
            }
        }
    }
}
