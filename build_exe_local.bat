@echo off
chcp 65001 >nul
setlocal EnableExtensions

cd /d "%~dp0"
set "LOG_FILE=%~dp0build_exe.log"
echo ==== %date% %time% ==== > "%LOG_FILE%"

echo [1/5] 检查 uv...
set "UV_EXE="
where uv >nul 2>nul
if %errorlevel%==0 (
    set "UV_EXE=uv"
) else (
    if exist "%USERPROFILE%\.local\bin\uv.exe" set "UV_EXE=%USERPROFILE%\.local\bin\uv.exe"
)

if not defined UV_EXE (
    echo 未检测到 uv，开始自动安装...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex" >>"%LOG_FILE%" 2>&1
    where uv >nul 2>nul
    if %errorlevel%==0 (
        set "UV_EXE=uv"
    ) else (
        if exist "%USERPROFILE%\.local\bin\uv.exe" set "UV_EXE=%USERPROFILE%\.local\bin\uv.exe"
    )
)

if not defined UV_EXE (
    echo 安装 uv 失败。详见：%LOG_FILE%
    pause
    exit /b 1
)

echo [2/5] 同步依赖...
"%UV_EXE%" sync >>"%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo 依赖安装失败。详见：%LOG_FILE%
    pause
    exit /b 1
)

echo [3/5] 安装 PyInstaller...
"%UV_EXE%" run python -m pip install pyinstaller >>"%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo 安装 PyInstaller 失败。详见：%LOG_FILE%
    pause
    exit /b 1
)

echo [4/5] 打包 EXE...
"%UV_EXE%" run pyinstaller --noconfirm --onefile --windowed --name AttendanceAnalyzer --paths src src/attendance_tool/main.py >>"%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo 打包失败。详见：%LOG_FILE%
    pause
    exit /b 1
)

echo [5/5] 完成：dist\AttendanceAnalyzer.exe
echo 详细日志：%LOG_FILE%
pause
endlocal
