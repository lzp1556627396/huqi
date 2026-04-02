@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo [1/4] 检查 uv...
set "UV_EXE="
where uv >nul 2>nul
if %errorlevel%==0 (
    set "UV_EXE=uv"
) else (
    if exist "%USERPROFILE%\.local\bin\uv.exe" (
        set "UV_EXE=%USERPROFILE%\.local\bin\uv.exe"
    )
)

if not defined UV_EXE (
    echo 未检测到 uv，开始自动安装...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"

    where uv >nul 2>nul
    if %errorlevel%==0 (
        set "UV_EXE=uv"
    ) else (
        if exist "%USERPROFILE%\.local\bin\uv.exe" (
            set "UV_EXE=%USERPROFILE%\.local\bin\uv.exe"
        )
    )
)

if not defined UV_EXE (
    echo.
    echo 安装 uv 失败，请检查网络或 PowerShell 执行策略后重试。
    pause
    exit /b 1
)

echo [2/4] 同步依赖（首次会自动下载 Python 和依赖）...
"%UV_EXE%" sync
if errorlevel 1 (
    echo.
    echo 依赖同步失败，请检查网络后重试。
    pause
    exit /b 1
)

echo [3/4] 启动考勤工具 GUI...
"%UV_EXE%" run attendance-gui
if errorlevel 1 (
    echo.
    echo GUI 启动失败，请把窗口报错截图给我，我继续帮你修。
    pause
    exit /b 1
)

echo [4/4] 已退出程序。
endlocal
