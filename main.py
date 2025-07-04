import argparse
import csv
from tabulate import tabulate
from typing import List, Dict, Optional
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="CSV Filter and Aggregator")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--where", help="Filter condition (e.g. column=value or column>value)")
    parser.add_argument("--aggregate", help="Aggregation (e.g. column=avg|min|max)")
    return parser.parse_args()


def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def apply_filter(data: List[Dict[str, str]], condition: str) -> List[Dict[str, str]]:
    if not condition:
        return data

    if '>' in condition:
        col, val = condition.split('>', 1)
        return [row for row in data if float(row[col]) > float(val)]
    elif '<' in condition:
        col, val = condition.split('<', 1)
        return [row for row in data if float(row[col]) < float(val)]
    elif '=' in condition:
        col, val = condition.split('=', 1)
        return [row for row in data if row[col] == val]
    else:
        print(f"Invalid filter condition: {condition}", file=sys.stderr)
        return data


def aggregate(data: List[Dict[str, str]], agg: Optional[str]) -> None:
    if not agg:
        print(tabulate(data, headers="keys", tablefmt="grid"))
        return

    try:
        column, op = agg.split("=")
        values = [float(row[column]) for row in data]

        if op == "avg":
            result = sum(values) / len(values)
        elif op == "min":
            result = min(values)
        elif op == "max":
            result = max(values)
        else:
            print(f"Unsupported aggregation operator: {op}", file=sys.stderr)
            return

        print(tabulate([{op: result}], headers="keys", tablefmt="grid"))
    except Exception as e:
        print(f"Aggregation failed: {e}", file=sys.stderr)


def main():
    args = parse_args()
    data = read_csv(args.file)
    filtered = apply_filter(data, args.where)
    aggregate(filtered, args.aggregate)


if __name__ == '__main__':
    main()
