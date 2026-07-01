param(
    [string]$SdkRoot = "$env:LOCALAPPDATA\Android\Sdk"
)

$ErrorActionPreference = "Stop"

Write-Host "[1/6] Checking Java..."
if (-not $env:JAVA_HOME) {
    throw "JAVA_HOME is not set. Install JDK 17 and set JAVA_HOME."
}

Write-Host "[2/6] Creating SDK folder..."
New-Item -ItemType Directory -Path $SdkRoot -Force | Out-Null

$cmdToolsZip = Join-Path $env:TEMP "commandlinetools-win.zip"
$cmdToolsDest = Join-Path $SdkRoot "cmdline-tools\latest"

Write-Host "[3/6] Downloading Android command-line tools..."
Invoke-WebRequest -Uri "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip" -OutFile $cmdToolsZip

Write-Host "[4/6] Extracting command-line tools..."
$extractTemp = Join-Path $env:TEMP "android-cmdline-tools"
if (Test-Path $extractTemp) { Remove-Item $extractTemp -Recurse -Force }
Expand-Archive -Path $cmdToolsZip -DestinationPath $extractTemp -Force
New-Item -ItemType Directory -Path $cmdToolsDest -Force | Out-Null
Copy-Item "$extractTemp\cmdline-tools\*" $cmdToolsDest -Recurse -Force

$sdkmanager = Join-Path $cmdToolsDest "bin\sdkmanager.bat"
if (!(Test-Path $sdkmanager)) {
    throw "sdkmanager not found at $sdkmanager"
}

Write-Host "[5/6] Installing SDK packages..."
& $sdkmanager --sdk_root=$SdkRoot "platform-tools" "platforms;android-35" "build-tools;35.0.0"

Write-Host "[6/6] Writing local.properties..."
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
"sdk.dir=$($SdkRoot -replace '\\','\\\\')" | Out-File -FilePath (Join-Path $projectRoot "local.properties") -Encoding ascii -Force

Write-Host "Setup complete. Build command: .\gradlew.bat assembleDebug"
