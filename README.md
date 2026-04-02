# 考勤自动分析工具（Python + GUI）

这个项目用于自动处理考勤 Excel，按你的规则计算：

- 正班出勤时长（白班/夜班，正班最多 8 小时，含 1 小时休息）
- 加班时长（白班 18:00 后，夜班次日 05:00 后）
- 迟到/早退时长（单独一列）

处理后会在原表 `概况统计与打卡明细` 中，紧挨考勤概况区域新增三列：

- `正班出勤时长(小时)`
- `加班时长(小时)`
- `迟到早退时长`

## 项目结构

```text
.
├── pyproject.toml
├── README.md
├── scripts
│   └── build_windows_exe.bat
├── src
│   └── attendance_tool
│       ├── __init__.py
│       ├── calculator.py
│       ├── cli.py
│       ├── excel_processor.py
│       ├── gui.py
│       ├── main.py
│       ├── models.py
│       └── time_utils.py
└── tests
    └── test_calculator.py
```

## 本地运行

```bash
uv sync
uv run attendance-gui
```

或命令行处理：

```bash
uv run attendance-cli -i "/path/to/input.xlsx"
```

输出文件默认是：`原文件名_处理结果.xlsx`

## 规则说明（已实现）

### 白班

- 正班时间：`08:00-17:00`
- 休息：`1 小时`
- 正班上限：`8 小时`
- 加班起算：`18:00`
- 迟到：首次打卡晚于 `08:00`
- 早退：最后打卡早于 `17:00`

### 夜班

- 正班时间：`20:00-次日05:00`
- 休息：`1 小时`
- 正班上限：`8 小时`
- 加班起算：`次日05:00`
- 迟到：首次打卡晚于 `20:00`
- 早退：最后打卡早于 `次日05:00`

### 无打卡

- 正班时长 = `0`
- 加班时长 = `0`
- 迟到早退列显示 `无打卡记录`

### 非白班/夜班

- 正班时长 = `0`
- 加班时长 = `0`
- 迟到早退列显示 `非白班/夜班`

## 打包 Windows EXE

在 Windows 下执行：

```bat
scripts\build_windows_exe.bat
```

生成文件在 `dist\AttendanceAnalyzer.exe`

## 无开发环境也能打包（推荐）

如果 Windows 机器没有 Python/开发环境，可以用 GitHub Actions 云端打包：

1. 把项目上传到 GitHub 仓库
2. 进入仓库 `Actions` 页面
3. 选择 `Build Windows EXE`
4. 点击 `Run workflow`
5. 等待完成后，在该次运行的 `Artifacts` 下载 `AttendanceAnalyzer-windows-exe`
6. 解压后即可得到 `AttendanceAnalyzer.exe`，双击即可使用

## 测试

```bash
uv run pytest
```
# huqi
