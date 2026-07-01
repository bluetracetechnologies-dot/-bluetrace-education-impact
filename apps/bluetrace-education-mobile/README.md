# Bluetrace Education Mobile MVP

This folder contains a clean Android Kotlin source project (Jetpack Compose) for a Presidency-oriented education app MVP.

## Modules delivered in MVP
- Parent experience dashboard
- Student safety event timeline
- Teacher productivity quick metrics
- Management KPI snapshot cards

## Stack
- Kotlin
- Jetpack Compose + Material 3
- Android Gradle Plugin 8.5+
- Java 17

## Run locally
1. Install Android Studio (latest stable).
2. Open this folder in Android Studio: `apps/bluetrace-education-mobile`
3. Copy `local.properties.example` to `local.properties` and set `sdk.dir`.
4. Let Gradle sync complete.
5. Run on emulator/device.

## APK generation
- Debug APK: Build > Build APK(s)
- CLI debug APK: `./gradlew assembleDebug`
- Release APK: configure signing in `app/build.gradle.kts`, then run `./gradlew assembleRelease`

## CI Build (No local Android SDK needed)
- GitHub Actions workflow: `.github/workflows/android-apk.yml`
- Trigger: push to `main` with app changes or manual workflow dispatch
- Artifact: `bluetrace-education-debug-apk`

## Local quick test checklist
1. Confirm Java 17 is active.
2. Ensure Android SDK has platform 35 and build-tools 35.0.0.
3. Run `gradle -p . assembleDebug` inside this folder.
4. Install APK from `app/build/outputs/apk/debug/` on device.

## Notes
- This repository previously contained proposal artifacts; this app folder is a new execution-ready codebase foundation.
