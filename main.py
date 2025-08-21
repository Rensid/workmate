import argparse
import sys
from reports.average import AverageReport
from parser import load_logs
from tabulate import tabulate


REPORTS = {
    "average": AverageReport,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Анализ файла с логами")
    parser.add_argument("--file", nargs="+", required=True, help="Путь к файлу")
    parser.add_argument(
        "--report",
        required=True,
        choices=REPORTS.keys(),
        help=f"Вариант отчета. Из доступных {REPORTS}",
    )
    parser.add_argument("--date", help="Фильтр по дате")
    return parser.parse_args()


def main():
    args = parse_args()

    logs = load_logs(args.file, date_filter=args.date)
    report_class = REPORTS[args.report]
    report = report_class(logs)
    data = report.generate()

    headers = report.headers()
    print(tabulate(data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
