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
    parser.add_argument("--order-by", help="Ordering (e.g. column=asc|desc)")
    return parser.parse_args()


def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def apply_filter(data: List[Dict[str, str]], condition: Optional[str]) -> List[Dict[str, str]]:
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


def apply_order(data: List[Dict[str, str]], order_clause: Optional[str]) -> List[Dict[str, str]]:
    if not order_clause:
        return data
    try:
        col, direction = order_clause.split("=")
        return sorted(data, key=lambda row: row[col] if not row[col].replace('.', '', 1).isdigit() else float(row[col]), reverse=(direction == "desc"))
    except Exception as e:
        print(f"Ordering failed: {e}", file=sys.stderr)
        return data


def aggregate(data: List[Dict[str, str]], agg: Optional[str]) -> None:
    if not agg:
        print(tabulate(data, headers="keys", tablefmt="grid"))
        return

    AGGREGATORS = {
        "avg": lambda vals: sum(vals) / len(vals),
        "min": min,
        "max": max
    }

    try:
        column, op = agg.split("=")
        values = [float(row[column]) for row in data]
        if op in AGGREGATORS:
            result = AGGREGATORS[op](values)
            print(tabulate([{op: result}], headers="keys", tablefmt="grid"))
        else:
            print(f"Unsupported aggregation operator: {op}", file=sys.stderr)
    except Exception as e:
        print(f"Aggregation failed: {e}", file=sys.stderr)


def main():
    args = parse_args()
    data = read_csv(args.file)
    filtered = apply_filter(data, args.where)
    ordered = apply_order(filtered, args.order_by)
    aggregate(ordered, args.aggregate)


if __name__ == '__main__':
    main()
