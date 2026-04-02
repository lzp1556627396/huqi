from __future__ import annotations

import argparse

from .excel_processor import process_workbook


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="考勤 Excel 自动分析工具")
    parser.add_argument("-i", "--input", required=True, help="输入 Excel 文件路径")
    parser.add_argument("-o", "--output", help="输出 Excel 文件路径")
    parser.add_argument(
        "-s",
        "--sheet",
        default="概况统计与打卡明细",
        help="要处理的工作表名称，默认：概况统计与打卡明细",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    output_path = process_workbook(
        input_file=args.input,
        output_file=args.output,
        sheet_name=args.sheet,
    )
    print(f"处理完成：{output_path}")


if __name__ == "__main__":
    main()

