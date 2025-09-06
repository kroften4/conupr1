import calendar
import datetime as dt

def cal_header(month: int, year: int) -> str:
    month_name = calendar.month_name[month]
    first_line = f"{month_name} {year}"
    free_space = 20 - len(first_line)
    leftpad = free_space // 2
    rightpad = free_space // 2
    if free_space % 2 != 0:
        leftpad += 1
    first_line = " " * leftpad + first_line + " " * rightpad
    return f"{first_line}\nMo Tu We Th Fr Sa Su\n"

def month_cal(month: int, year: int) -> str:
    output = cal_header(month, year)
    for week in calendar.monthcalendar(year, month):
        week_days: list[str] = []
        for day in week:
            day = str(day)
            if day == "0":
                day = "  "
            if len(day) == 1:
                day = " " + day
            week_days.append(day)
        output += " ".join(week_days) + "\n"
    return output

def month_join(month1: str, month2: str, separator: str):
    if (month1 == ""):
        return month2
    lines1 = month1.split("\n")[:-1]
    lines2 = month2.split("\n")[:-1]
    empty_line = " " * 20
    if len(lines1) > len(lines2):
        lines2 += [empty_line] * (len(lines1) - len(lines2))
    elif len(lines2) > len(lines1):
        lines1 += [empty_line] * (len(lines2) - len(lines1))
    result: list[str] = []
    for line1, line2 in zip(lines1, lines2):
        result.append(line1 + separator + line2)
    return "\n".join(result) + "\n"

def multimonth_cal(month_start: int, year_start: int, month_number: int) -> str:
    output: str = ""
    for i in range(month_start, month_start + month_number, 3):
        month_line: str = ""
        n = 3
        if i + 3 > month_start + month_number:
            n = (month_start + month_number) % 3 + 1
        for month_num in range(i, i + n):
            year = year_start + month_num // 12
            month = month_cal((month_num % 12 or 12), year)
            month_line = month_join(month_line, month, "  ")
        output += month_line
    return output
