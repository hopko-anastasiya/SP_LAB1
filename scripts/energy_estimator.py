import csv
import statistics

P_IDLE = 12.0
P_LOAD = 42.0
DELTA_P = P_LOAD - P_IDLE

def get_mean_times(csv_path):
    real_times, user_times = [], []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            real_times.append(float(row['real_sec']))
            user_times.append(float(row['user_sec']))
    return statistics.mean(real_times), statistics.mean(user_times)

slow_real, slow_user = get_mean_times('results/measurements_slow.csv')
fast_real, fast_user = get_mean_times('results/measurements_fast.csv')

e_sys_slow = P_LOAD * slow_real
e_sys_fast = P_LOAD * fast_real

e_prog_slow = DELTA_P * slow_user
e_prog_fast = DELTA_P * fast_user

col_w = [34, 23, 23, 21]

def make_row(c0, c1, c2, c3):
    return f"| {c0:<{col_w[0]}} | {c1:^{col_w[1]}} | {c2:^{col_w[2]}} | {c3:^{col_w[3]}} |"

header = make_row("Показник енерговитрат", "Базова версія", "Оптимізована", "Економія / Прискорення")
sep_line = f"|{'-'*(col_w[0]+2)}|{'-'*(col_w[1]+2)}|{'-'*(col_w[2]+2)}|{'-'*(col_w[3]+2)}|"

output_lines = [
    "\nОцінка та порівняння енерговитрат\n",
    f"> Розрахунок виконано за аналітичною моделлю динамічної потужності (P_load = {P_LOAD} Вт, P_idle = {P_IDLE} Вт).\n",
    sep_line,
    header,
    sep_line,
    make_row("Час виконання (Elapsed Real Time)", f"{slow_real:.4f} с", f"{fast_real:.4f} с", f"{slow_real/fast_real:.2f}x швидше"),
    make_row("Час CPU (User CPU Time)", f"{slow_user:.4f} с", f"{fast_user:.4f} с", f"{slow_user/fast_user:.2f}x швидше"),
    make_row("Енергія системи (п. 3.1)", f"{e_sys_slow:.2f} Дж", f"{e_sys_fast:.2f} Дж", f"{e_sys_slow/e_sys_fast:.2f}x менше"),
    make_row("Енергія процесу (п. 3.2)", f"{e_prog_slow:.2f} Дж", f"{e_prog_fast:.2f} Дж", f"{e_prog_slow/e_prog_fast:.2f}x менше"),
    sep_line
]

full_report = "\n".join(output_lines)
print(full_report)

out_file = 'results/energy_report.md'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(full_report + "\n")
print(f"\nТаблицю збережено у файл: {out_file}")
