from zhdate import ZhDate
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width // 2 - size[0] // 2
    y = screen_height // 2 - size[1] // 2
    window.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

def get_shichen(hour):
    shichen_dict = {
        1: "子時 (23:00–01:00)",
        2: "丑時 (01:00–03:00)",
        3: "寅時 (03:00–05:00)",
        4: "卯時 (05:00–07:00)",
        5: "辰時 (07:00–09:00)",
        6: "巳時 (09:00–11:00)",
        7: "午時 (11:00–13:00)",
        8: "未時 (13:00–15:00)",
        9: "申時 (15:00–17:00)",
        10: "酉時 (17:00–19:00)",
        11: "戌時 (19:00–21:00)",
        12: "亥時 (21:00–23:00)",
    }

    if 23 <= hour or hour < 1:
        shichen_value = 1
    elif 1 <= hour < 3:
        shichen_value = 2
    elif 3 <= hour < 5:
        shichen_value = 3
    elif 5 <= hour < 7:
        shichen_value = 4
    elif 7 <= hour < 9:
        shichen_value = 5
    elif 9 <= hour < 11:
        shichen_value = 6
    elif 11 <= hour < 13:
        shichen_value = 7
    elif 13 <= hour < 15:
        shichen_value = 8
    elif 15 <= hour < 17:
        shichen_value = 9
    elif 17 <= hour < 19:
        shichen_value = 10
    elif 19 <= hour < 21:
        shichen_value = 11
    else:
        shichen_value = 12

    return shichen_value, shichen_dict[shichen_value]

def xiao_liu_ren(lunar_month, lunar_day, current_shichen):
    liuren_table = ["大安", "留連", "速喜", "赤口", "小吉", "空亡"]

    month_position = (lunar_month - 1) % 6
    month_xiao_liu_ren = liuren_table[month_position]

    day_position = (month_position + (lunar_day - 1)) % 6
    day_xiao_liu_ren = liuren_table[day_position]

    shichen_position = (day_position + (current_shichen - 1)) % 6
    shichen_xiao_liu_ren = liuren_table[shichen_position]

    return {
        "month_xiao_liu_ren": month_xiao_liu_ren,
        "day_xiao_liu_ren": day_xiao_liu_ren,
        "shichen_xiao_liu_ren": shichen_xiao_liu_ren,
    }

def show_result(current_date, lunar_date):
    try:
        lunar_Year = lunar_date.lunar_year
        lunar_month = lunar_date.lunar_month
        lunar_day = lunar_date.lunar_day

        shichen_value, shichen_name = get_shichen(current_date.hour)

        result = (
            f"國曆：{current_date.year}年{current_date.month}月{current_date.day}日{current_date.hour}點\n"
            f"農曆：{lunar_Year}年{lunar_month}月{lunar_day}日 {shichen_name}\n"
        )

        xiao_liu_ren_result = xiao_liu_ren(lunar_month, lunar_day, shichen_value)

        result += (
            f"月份小六壬：{xiao_liu_ren_result['month_xiao_liu_ren']}\n"
            f"日期小六壬：{xiao_liu_ren_result['day_xiao_liu_ren']}\n"
            f"時辰小六壬：{xiao_liu_ren_result['shichen_xiao_liu_ren']}"
        )

        # 創建結果視窗
        result_window = tk.Toplevel()
        result_window.title("結果")
        result_window.geometry("300x130")  
        center_window(result_window)

        def close_window():
            result_window.destroy()
            result_window.quit()

        result_window.protocol("WM_DELETE_WINDOW", close_window)  # 捕捉右上角 X 按鈕

        tk.Label(result_window, text=result, justify="left", padx=10, pady=10).pack()
        tk.Button(result_window, text="確定", command=close_window).pack()

        result_window.mainloop()
    except Exception as e:
        messagebox.showerror("錯誤", f"無法顯示結果：{e}")

def main():
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗

    current_date = None
    lunar_date = None

    choice = messagebox.askquestion("選擇模式", "是否使用當前時間？\n是=使用當前時間，否=自訂義時間")

    if choice == "yes":
        try:
            current_date = datetime.now()
            lunar_date = ZhDate.today()
            show_result(current_date, lunar_date)
        except Exception as e:
            messagebox.showerror("錯誤", f"計算當前時間時出現錯誤：{e}")

    else:
        def submit():
            try:
                if not year_entry.get() or not month_entry.get() or not day_entry.get() or not hour_entry.get():
                    messagebox.showwarning("提示", "請輸入完整的資料或按右上角 X 離開")
                    return
                
                year = int(year_entry.get())
                month = int(month_entry.get())
                day = int(day_entry.get())
                hour = int(hour_entry.get())

                if not (1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23):
                    raise ValueError("日期或時間不正確！")

                if not (1900 <= year <= 2100):
                    raise ValueError("日期超出農曆支持範圍！")

                nonlocal current_date, lunar_date
                current_date = datetime(year, month, day, hour)
                lunar_date = ZhDate.from_datetime(current_date)
                input_frame.destroy()
                show_result(current_date, lunar_date)
            except ValueError as e:
                messagebox.showerror("錯誤", str(e))


        input_frame = tk.Toplevel(root)
        input_frame.title("自訂義時間")
        input_frame.geometry("200x120")  
        center_window(input_frame)


        tk.Label(input_frame, text="年份：").grid(row=0, column=0)
        year_entry = tk.Entry(input_frame ,  width=8)
        year_entry.grid(row=0, column=1, sticky="w", pady=2, padx=5)

        tk.Label(input_frame, text="月份：").grid(row=1, column=0)
        month_entry = tk.Entry(input_frame ,  width=8)
        month_entry.grid(row=1, column=1, sticky="w", pady=2, padx=5)

        tk.Label(input_frame, text="日期：").grid(row=2, column=0)
        day_entry = tk.Entry(input_frame ,  width=8)
        day_entry.grid(row=2, column=1, sticky="w", pady=2, padx=5)

        tk.Label(input_frame, text="時間（24小時制）：").grid(row=3, column=0)
        hour_entry = tk.Entry(input_frame ,  width=8)
        hour_entry.grid(row=3, column=1, sticky="w", pady=2, padx=5)

        tk.Button(input_frame, text="提交", command=submit).grid(row=4, columnspan=2)

        input_frame.wait_window()

if __name__ == "__main__":
    main()
