@echo off
setlocal
set APP_HOME=%~dp0
set PROPERTIES_FILE=%APP_HOME%gradle\wrapper\gradle-wrapper.properties
if not exist "%PROPERTIES_FILE%" (
  echo Missing %PROPERTIES_FILE% 1>&2
  exit /b 1
)
for /f "tokens=2 delims==" %%A in ('findstr /b "distributionUrl=" "%PROPERTIES_FILE%"') do set DISTRIBUTION_URL=%%A
set DISTRIBUTION_URL=%DISTRIBUTION_URL:\:=:%
for /f "tokens=2 delims=-" %%A in ("%DISTRIBUTION_URL%") do set GRADLE_VERSION=%%A
if "%GRADLE_USER_HOME%"=="" set GRADLE_USER_HOME=%APP_HOME%.gradle
set DIST_DIR=%GRADLE_USER_HOME%\wrapper\dists
set ZIP=%DIST_DIR%\gradle-%GRADLE_VERSION%-bin.zip
set GRADLE_HOME=%DIST_DIR%\gradle-%GRADLE_VERSION%
set GRADLE_BIN=%GRADLE_HOME%\bin\gradle.bat
if not exist "%GRADLE_BIN%" (
  mkdir "%DIST_DIR%" 2>nul
  if not exist "%ZIP%" powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%DISTRIBUTION_URL%' -OutFile '%ZIP%'"
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Force '%ZIP%' '%DIST_DIR%'"
)
call "%GRADLE_BIN%" %*
