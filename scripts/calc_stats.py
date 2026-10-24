import sys
import csv
import math
import statistics

if len(sys.argv) < 2:
    print("Використання: python3 scripts/calc_stats.py <шлях_до_файлу.csv>")
    sys.exit(1)

csv_file = sys.argv[1]

data = {
    'real_sec': [],
    'user_sec': [],
    'sys_sec': [],
    'max_rss_kb': [],
    'page_faults': [],
    'context_switches': []
}

labels = {
    'real_sec': 'Elapsed Real Time (с)',
    'user_sec': 'User CPU Time (с)',
    'sys_sec': 'System CPU Time (с)',
    'max_rss_kb': 'Max RSS Memory (КБ)',
    'page_faults': 'Minor Page Faults',
    'context_switches': 'Context Switches'
}

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for k in data.keys():
            if k in row and row[k] != '':
                data[k].append(float(row[k]))

n = len(data['real_sec'])
if n < 2:
    print("Недостатньо даних")
    sys.exit(1)

t_val = 2.045 if n == 30 else 2.0

col_w = [25, 16, 17, 23, 26]

def make_row(c0, c1, c2, c3, c4):
    return f"| {c0:<{col_w[0]}} | {c1:>{col_w[1]}} | {c2:>{col_w[2]}} | {c3:>{col_w[3]}} | {c4:^{col_w[4]}} |"

header = make_row("Метрика", "Середнє", "Дисперсія", "Сер. відхил.", "95% Довірчий інтервал")
sep_line = f"|{'-'*(col_w[0]+2)}|{'-'*(col_w[1]+2)}|{'-'*(col_w[2]+2)}|{'-'*(col_w[3]+2)}|{'-'*(col_w[4]+2)}|"

output_lines = [
    f"\nРезультат: {csv_file} (N = {n})\n",
    sep_line,
    header,
    sep_line
]

for k, vals in data.items():
    if not vals:
        continue
    mean_val = statistics.mean(vals)
    var_val = statistics.variance(vals)
    std_val = statistics.stdev(vals)
    margin = t_val * (std_val / math.sqrt(n))
    ci_low = mean_val - margin
    ci_high = mean_val + margin

    if "Time" in labels[k]:
        c1 = f"{mean_val:.4f}"
        c2 = f"{var_val:.6f}"
        c3 = f"{std_val:.4f}"
        c4 = f"[{ci_low:.4f}; {ci_high:.4f}]"
    else:
        c1 = f"{mean_val:.2f}"
        c2 = f"{var_val:.2f}"
        c3 = f"{std_val:.2f}"
        c4 = f"[{ci_low:.2f}; {ci_high:.2f}]"

    output_lines.append(make_row(labels[k], c1, c2, c3, c4))

output_lines.append(sep_line)

full_table = "\n".join(output_lines)
print(full_table)

out_md = csv_file.replace("measurements_", "stats_").replace(".csv", ".md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write(full_table + "\n")
print(f"\nТаблицю збережено у файл: {out_md}")
