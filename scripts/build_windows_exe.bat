@echo off
chcp 65001 >nul
setlocal

echo [1/4] 安装项目依赖...
python -m pip install -U pip
python -m pip install .
python -m pip install pyinstaller

echo [2/4] 清理旧构建...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [3/4] 生成 EXE...
pyinstaller ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name AttendanceAnalyzer ^
  --paths src ^
  src\attendance_tool\main.py

echo [4/4] 完成
echo 输出文件：dist\AttendanceAnalyzer.exe
pause

