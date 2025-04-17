import tkinter as tk
from tkinter import ttk, messagebox

class WarehouseCalculator:
    def __init__(self, root):
        self.root = root
        root.title("Калькулятор склада")
        
        # Настройка масштабирования главного окна
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Инициализация переменных
        self.qcr = []
        self.T = []
        self.p = []
        self.Vck1 = []
        self.Vck2 = []
        self.kpi = []
        self.Fck1 = []
        self.Fck2 = []
        self.Qci = []
        self.Fnc1 = []
        self.Fnc2 = []
        self.V_goods = []
        self.vg_T = []

        # Константы
        self.kckmin = 0.8
        self.kckmax = 0.9
        self.knmin = 1.1
        self.knmax = 1.5

        # Создание основного фрейма с отступами
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка масштабирования основного фрейма
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)  # Индекс строки с текстовым полем

        current_row = 0

        # Поля ввода с описаниями
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=current_row, column=0, columnspan=2, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, 
                 text="Количество поступающих грузов:",
                 wraplength=300).grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=2)
        self.num_goods = ttk.Entry(input_frame)
        self.num_goods.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        current_row += 1

        ttk.Label(input_frame, 
                 text="Ширина склада (метры):",
                 wraplength=300).grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=2)
        self.width_entry = ttk.Entry(input_frame)
        self.width_entry.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        current_row += 1

        ttk.Label(input_frame, 
                 text="Расчетная эксплуатационная нагрузка (т/м²):",
                 wraplength=300).grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=2)
        self.P = ttk.Entry(input_frame)
        self.P.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        current_row += 1

        # Выбор типа груза
        ttk.Label(input_frame, 
                 text="Тип груза:\n1 - однородные крупногабаритные грузы\n2 - мелкопартионные грузы",
                 wraplength=300, justify="left").grid(row=current_row, column=0, sticky=tk.W, padx=5, pady=2)
        self.goods_type = ttk.Combobox(input_frame, 
                                      values=["1 - однородные крупногабаритные", 
                                             "2 - мелкопартионные"])
        self.goods_type.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        current_row += 1

        # Кнопка начала расчета
        ttk.Button(main_frame, 
                  text="Начать расчет", 
                  command=self.start_calculation).grid(row=current_row, 
                                                     column=0, 
                                                     columnspan=2, 
                                                     pady=10)
        current_row += 1

        # Создание фрейма для текстового поля с полосой прокрутки
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=current_row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Добавление полосы прокрутки
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Область вывода результатов с привязкой к полосе прокрутки
        self.result_text = tk.Text(text_frame, height=20, width=70, yscrollcommand=scrollbar.set)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.result_text.yview)

    def parse_float(self, value):
        """Преобразует строку с числом в float, поддерживая и запятую, и точку как разделитель"""
        try:
            # Заменяем запятую на точку
            value = value.replace(',', '.')
            return float(value)
        except ValueError:
            return None

    def validate_positive(self, value, message):
        """Проверяет, что значение является положительным числом"""
        try:
            num = self.parse_float(value)
            if num is None or num <= 0:
                messagebox.showerror("Ошибка", f"{message} должно быть положительным числом")
                return False
            return num
        except Exception:
            messagebox.showerror("Ошибка", "Введите числовое значение")
            return False

    def get_input_series(self, title, count, message):
        """Получает серию значений от пользователя"""
        values = []
        input_window = tk.Toplevel(self.root)
        input_window.title(title)

        # Словарь с описаниями и единицами измерения
        descriptions = {
            "Ввод грузопотока": "Расчётный суточный грузопоток (тонн/сутки)",
            "Ввод сроков хранения": "Срок хранения груза (сутки)",
            "Ввод удельной нагрузки": "Удельная нагрузка на пол склада (тонн/м²)",
            "Ввод коэффициентов проездов": "Коэффициент площади проездов:\n1.7 - для крытых складов и платформ\n2.0 - для мелких отправок\n1.9 - для контейнерных площадок\n1.6 - для тяжеловесных грузов\n1.5 - для складов угля и стройматериалов",
            "Ввод среднесуточного поступления": "Среднесуточное поступление/отпуск материала (тонн/сутки)"
        }
        
        # Добавляем описание в верхней части окна
        if title in descriptions:
            ttk.Label(input_window, text=descriptions[title], wraplength=400, justify="left").grid(
                row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
            start_row = 1
        else:
            start_row = 0
        
        entries = []
        for i in range(count):
            ttk.Label(input_window, text=f"Груз {i+1}:").grid(
                row=i+start_row, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(input_window)
            entry.grid(row=i+start_row, column=1, padx=5, pady=2)
            entries.append(entry)

        def collect_values():
            nonlocal values
            values = []
            for entry in entries:
                value = self.validate_positive(entry.get(), message)
                if value:
                    values.append(value)
                else:
                    return
            input_window.destroy()

        ttk.Button(input_window, text="OK", command=collect_values).grid(
            row=count+start_row, column=0, columnspan=2, pady=10)
        
        # Центрируем окно относительно главного окна
        input_window.transient(self.root)
        input_window.grab_set()
        self.root.wait_window(input_window)
        return values

    def start_calculation(self):
        try:
            # Проверка начальных данных
            num_goods = self.validate_positive(self.num_goods.get(), "Количество грузов")
            if not num_goods:
                return
            
            width = self.validate_positive(self.width_entry.get(), "Ширина склада")
            if not width:
                return
                
            # Установка коэффициента использования площади
            if width < 24:
                self.kip = 0.65 if self.goods_type.get()[0] == "1" else 0.55
            elif width < 30:
                self.kip = 0.7 if self.goods_type.get()[0] == "1" else 0.6
            else:
                self.kip = 0.75 if self.goods_type.get()[0] == "1" else 0.65

            # Очистка текстового поля перед новым расчетом
            self.result_text.delete(1.0, tk.END)

            # Получение данных через диалоговые окна
            self.qcr = self.get_input_series("Ввод грузопотока", 
                                           int(num_goods), 
                                           "Грузопоток")
            if not self.qcr:
                return
                
            self.T = self.get_input_series("Ввод сроков хранения", 
                                          int(num_goods),
                                          "Срок хранения")
            if not self.T:
                return
                
            self.p = self.get_input_series("Ввод удельной нагрузки", 
                                          int(num_goods),
                                          "Удельная нагрузка")
            if not self.p:
                return

            # Расчет и вывод результатов в порядке
            self.calculate_vck()      # 1. Вместимость склада
            self.calculate_fck()      # 2. Ориентировочная площадь (запускает calculate_fnc после завершения)
            # Остальные расчеты будут вызваны последовательно в предыдущих методах
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при расчетах: {str(e)}")

    def calculate_vck(self):
        self.Vck1 = [self.kckmin * q * t for q, t in zip(self.qcr, self.T)]
        self.Vck2 = [self.kckmax * q * t for q, t in zip(self.qcr, self.T)]
        
        self.result_text.insert(tk.END, "1. Вместимость склада:\n")
        self.result_text.insert(tk.END, "-" * 50 + "\n")
        self.result_text.insert(tk.END, f"При минимальном коэффициенте складируемости (0.8): {sum(self.Vck1):.2f} тонн\n")
        self.result_text.insert(tk.END, f"При максимальном коэффициенте складируемости (0.9): {sum(self.Vck2):.2f} тонн\n\n")

    def calculate_fck(self):
        # Создаем окно для выбора коэффициентов
        coef_window = tk.Toplevel(self.root)
        coef_window.title("Выбор коэффициентов проездов")
        
        # Словарь коэффициентов с описаниями
        coefficients = {
            "1.7": "для крытых складов и платформ при хранении тарных и штучных грузов (повагонные отправки)",
            "2.0": "для складов тарно-штучных грузов (мелкие отправки)",
            "1.9": "для контейнерных площадок",
            "1.6": "для площадок тяжеловесных грузов и лесоматериалов",
            "1.5": "для складов угля и минерально-строительных материалов"
        }
        
        self.kpi = []  # Очищаем список перед заполнением
        row = 0
        
        # Создаем метку с пояснением
        ttk.Label(coef_window, 
                 text="Выберите коэффициент для каждого груза:",
                 wraplength=400).grid(row=row, column=0, columnspan=2, padx=5, pady=5)
        row += 1
        
        # Создаем список Combobox'ов для каждого груза
        comboboxes = []
        for i in range(len(self.qcr)):
            ttk.Label(coef_window, 
                     text=f"Груз {i+1}:").grid(row=row, column=0, padx=5, pady=2)
            
            # Создаем строки для комбобокса в формате "1.7 - для крытых складов..."
            combo_values = [f"{k} - {v}" for k, v in coefficients.items()]
            combo = ttk.Combobox(coef_window, values=combo_values, width=70)
            combo.grid(row=row, column=1, padx=5, pady=2)
            combo.set(combo_values[0])  # Устанавливаем первое значение по умолчанию
            comboboxes.append(combo)
            row += 1
        
        def collect_coefficients():
            try:
                # Получаем числовые значения из выбранных строк (берем первые 3 символа и преобразуем в float)
                self.kpi = [float(box.get()[:3]) for box in comboboxes]
                
                # Рассчитываем площади
                self.Fck1 = [k * ((self.kckmin * q * t) / p) 
                            for k, q, t, p in zip(self.kpi, self.qcr, self.T, self.p)]
                self.Fck2 = [k * ((self.kckmax * q * t) / p)
                            for k, q, t, p in zip(self.kpi, self.qcr, self.T, self.p)]
                
                # Выводим результаты
                self.result_text.insert(tk.END, "2. Ориентировочная площадь склада:\n")
                self.result_text.insert(tk.END, "-" * 50 + "\n")
                self.result_text.insert(tk.END, f"При минимальном коэффициенте складируемости (0.8): {sum(self.Fck1):.2f} м²\n")
                self.result_text.insert(tk.END, f"При максимальном коэффициенте складируемости (0.9): {sum(self.Fck2):.2f} м²\n\n")
                
                coef_window.destroy()
                # После закрытия окна коэффициентов вызываем calculate_fnc
                self.calculate_fnc()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при расчете: {str(e)}")
        
        ttk.Button(coef_window, text="Рассчитать",
                  command=collect_coefficients).grid(row=row, column=0, columnspan=2, pady=10)
        
        coef_window.transient(self.root)
        coef_window.grab_set()

    def calculate_fnc(self):
        # Создаем окно для ввода среднесуточного поступления
        input_window = tk.Toplevel(self.root)
        input_window.title("Ввод среднесуточного поступления")
        
        row = 0
        # Добавляем описание
        ttk.Label(input_window, 
                 text="Среднесуточное поступление/отпуск материала (тонн/сутки)",
                 wraplength=300).grid(row=row, column=0, columnspan=2, padx=5, pady=5)
        row += 1
        
        # Создаем поля ввода
        entries = []
        for i in range(len(self.qcr)):
            ttk.Label(input_window, text=f"Груз {i+1}:").grid(
                row=row, column=0, padx=5, pady=2)
            entry = ttk.Entry(input_window)
            entry.grid(row=row, column=1, padx=5, pady=2)
            entries.append(entry)
            row += 1

        def collect_values():
            try:
                self.Qci = []
                for entry in entries:
                    value = self.validate_positive(entry.get(), "Среднесуточное поступление")
                    if value:
                        self.Qci.append(value)
                    else:
                        return
                
                self.Fnc1 = [(self.knmin * q * t) / p 
                            for q, t, p in zip(self.Qci, self.T, self.p)]
                self.Fnc2 = [(self.knmax * q * t) / p
                            for q, t, p in zip(self.Qci, self.T, self.p)]
                
                self.result_text.insert(tk.END, "3. Площадь приёмо-сортировочных, комплектовочных площадок:\n")
                self.result_text.insert(tk.END, "-" * 50 + "\n")
                self.result_text.insert(tk.END, f"При минимальном коэффициенте складируемости (0.8): {sum(self.Fnc1):.2f} м²\n")
                self.result_text.insert(tk.END, f"При максимальном коэффициенте складируемости (0.9): {sum(self.Fnc2):.2f} м²\n\n")
                
                input_window.destroy()
                # После закрытия окна ввода среднесуточного поступления продолжаем расчеты
                self.calculate_fpol()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при расчете: {str(e)}")

        ttk.Button(input_window, text="OK", 
                  command=collect_values).grid(row=row, column=0, columnspan=2, pady=10)
        
        input_window.transient(self.root)
        input_window.grab_set()

    def calculate_fpol(self):
        try:
            # Проверяем, что P введено и является положительным числом
            P = self.validate_positive(self.P.get(), "Расчетная эксплуатационная нагрузка")
            if not P:
                raise ValueError("Некорректное значение расчетной эксплуатационной нагрузки")
            
            Fpol1 = sum(self.Vck1) / (self.kip * P)
            Fpol2 = sum(self.Vck2) / (self.kip * P)
            
            self.result_text.insert(tk.END, "4. Полезная площадь склада:\n")
            self.result_text.insert(tk.END, "-" * 50 + "\n")
            self.result_text.insert(tk.END, f"При минимальном коэффициенте складируемости (0.8): {Fpol1:.2f} м²\n")
            self.result_text.insert(tk.END, f"При максимальном коэффициенте складируемости (0.9): {Fpol2:.2f} м²\n\n")
            
            # После расчета полезной площади открываем окно для ввода параметров общей площади
            self.get_general_area_parameters()
            
            return Fpol1, Fpol2
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете полезной площади: {str(e)}")
            return 0, 0

    def get_general_area_parameters(self):
        # Создаем окно для ввода параметров общей площади
        params_window = tk.Toplevel(self.root)
        params_window.title("Параметры для расчета общей площади")
        
        row = 0
        # Добавляем описание
        ttk.Label(params_window, 
                 text="Введите параметры для расчета общей площади склада:",
                 wraplength=300).grid(row=row, column=0, columnspan=2, padx=5, pady=5)
        row += 1
        
        # Создаем поля ввода
        ttk.Label(params_window, text="Вместимость штабеля/стеллажа (тонн):").grid(
            row=row, column=0, padx=5, pady=2)
        self.dV = ttk.Entry(params_window)
        self.dV.grid(row=row, column=1, padx=5, pady=2)
        row += 1
        
        ttk.Label(params_window, text="Длина штабеля (м):").grid(
            row=row, column=0, padx=5, pady=2)
        self.L = ttk.Entry(params_window)
        self.L.grid(row=row, column=1, padx=5, pady=2)
        row += 1
        
        ttk.Label(params_window, text="Ширина штабеля (м):").grid(
            row=row, column=0, padx=5, pady=2)
        self.W = ttk.Entry(params_window)
        self.W.grid(row=row, column=1, padx=5, pady=2)
        row += 1

        def collect_and_calculate():
            try:
                # Проверяем введенные значения
                dV = self.validate_positive(self.dV.get(), "Вместимость штабеля")
                L = self.validate_positive(self.L.get(), "Длина штабеля")
                W = self.validate_positive(self.W.get(), "Ширина штабеля")
                
                if all([dV, L, W]):
                    params_window.destroy()
                    self.calculate_fobsh_with_params(dV, L, W)
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при вводе параметров: {str(e)}")

        ttk.Button(params_window, text="Рассчитать", 
                  command=collect_and_calculate).grid(
            row=row, column=0, columnspan=2, pady=10)
        
        params_window.transient(self.root)
        params_window.grab_set()

    def calculate_fobsh_with_params(self, dV, L, W):
        try:
            kip = self.kip
            nl1 = sum(self.Vck1) / dV
            nl2 = sum(self.Vck2) / dV
            deltaF = L * W * kip
            self.fobsh1 = nl1 * deltaF  # Сохраняем значения как атрибуты класса
            self.fobsh2 = nl2 * deltaF
            
            self.result_text.insert(tk.END, "5. Общая площадь склада:\n")
            self.result_text.insert(tk.END, "-" * 50 + "\n")
            self.result_text.insert(tk.END, f"При минимальном коэффициенте складируемости (0.8): {self.fobsh1:.2f} м²\n")
            self.result_text.insert(tk.END, f"При максимальном коэффициенте складируемости (0.9): {self.fobsh2:.2f} м²\n\n")
            
            # После расчета общей площади открываем окно для ввода дополнительных параметров
            self.get_additional_data_and_calculate_coefficients()
            
            return self.fobsh1, self.fobsh2
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете общей площади: {str(e)}")
            return 0, 0

    def calculate_coefficients(self):
        try:
            # Проверка введенных значений
            if not all(self.validate_positive(entry.get(), "Значение") for entry in 
                      [self.Fl, self.Vf, self.Qn, self.Qot, self.T_koef]):
                return
            
            # Расчет коэффициентов
            koef_results = self.f_koef()
            
            # Вывод результатов в основное окно
            self.result_text.insert(tk.END, "6. Расчетные коэффициенты:\n")
            self.result_text.insert(tk.END, "-" * 50 + "\n")
            self.result_text.insert(tk.END, "Коэффициент использования площади склада:\n")
            self.result_text.insert(tk.END, f"  При минимальном коэффициенте складируемости (0.8): {koef_results['k_use_space1']:.2f}\n")
            self.result_text.insert(tk.END, f"  При максимальном коэффициенте складируемости (0.9): {koef_results['k_use_space2']:.2f}\n\n")
            
            self.result_text.insert(tk.END, "Коэффициент использования объема склада:\n")
            self.result_text.insert(tk.END, f"  При минимальном коэффициенте складируемости (0.8): {koef_results['k_use_v1']:.2f}\n")
            self.result_text.insert(tk.END, f"  При максимальном коэффициенте складируемости (0.9): {koef_results['k_use_v2']:.2f}\n\n")
            
            self.result_text.insert(tk.END, "Коэффициент оборачиваемости склада:\n")
            self.result_text.insert(tk.END, f"  При минимальном коэффициенте складируемости (0.8): {koef_results['k_ob1']:.2f}\n")
            self.result_text.insert(tk.END, f"  При максимальном коэффициенте складируемости (0.9): {koef_results['k_ob2']:.2f}\n\n")
            
            self.result_text.insert(tk.END, "Коэффициент грузопереработки:\n")
            self.result_text.insert(tk.END, f"  При минимальном коэффициенте складируемости (0.8): {koef_results['Qck1']:.2f}\n")
            self.result_text.insert(tk.END, f"  При максимальном коэффициенте складируемости (0.9): {koef_results['Qck2']:.2f}\n")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете коэффициентов: {str(e)}")

    def get_additional_data_and_calculate_coefficients(self):
        # Создание окна для ввода дополнительных параметров
        input_window = tk.Toplevel(self.root)
        input_window.title("Дополнительные параметры для расчета")
        
        # Добавление полей ввода
        row = 0
        
        # Поля для расчета коэффициентов
        ttk.Label(input_window, text="Площадь, занятая грузом (м²):").grid(row=row, column=0, padx=5, pady=2)
        self.Fl = ttk.Entry(input_window)
        self.Fl.grid(row=row, column=1, padx=5, pady=2)
        row += 1
        
        ttk.Label(input_window, text="Среднее количество грузов (тонн):").grid(row=row, column=0, padx=5, pady=2)
        self.Vf = ttk.Entry(input_window)
        self.Vf.grid(row=row, column=1, padx=5, pady=2)
        row += 1
        
        ttk.Label(input_window, text="Поступление грузов (тонн):").grid(row=row, column=0, padx=5, pady=2)
        self.Qn = ttk.Entry(input_window)
        self.Qn.grid(row=row, column=1, padx=5, pady=2)
        row += 1
        
        ttk.Label(input_window, text="Отпуск грузов (тонн):").grid(row=row, column=0, padx=5, pady=2)
        self.Qot = ttk.Entry(input_window)
        self.Qot.grid(row=row, column=1, padx=5, pady=2)
        row += 1
        
        ttk.Label(input_window, text="Период времени (сутки):").grid(row=row, column=0, padx=5, pady=2)
        self.T_koef = ttk.Entry(input_window)
        self.T_koef.grid(row=row, column=1, padx=5, pady=2)
        row += 1

        # Добавляем поле для ввода объема грузов
        self.V_goods = []
        for i in range(len(self.qcr)):
            ttk.Label(input_window, text=f"Объем груза {i+1} (тонн):").grid(row=row, column=0, padx=5, pady=2)
            v_entry = ttk.Entry(input_window)
            v_entry.grid(row=row, column=1, padx=5, pady=2)
            self.V_goods.append(v_entry)
            row += 1
        
        def collect_and_calculate():
            try:
                # Проверка всех введенных значений
                entries = [self.Fl, self.Vf, self.Qn, self.Qot, self.T_koef]
                entries.extend(self.V_goods)
                
                if not all(self.validate_positive(entry.get(), "Значение") for entry in entries):
                    return
                
                # Преобразование значений объема грузов в числа
                self.V_goods = [float(entry.get()) for entry in self.V_goods]
                
                # Расчет коэффициентов
                self.calculate_coefficients()
                
                input_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при расчетах: {str(e)}")

        ttk.Button(input_window, text="Рассчитать", 
                  command=collect_and_calculate).grid(
            row=row, column=0, columnspan=2, pady=10)
        
        input_window.transient(self.root)
        input_window.grab_set()

    def f_koef(self):
        try:
            # Проверяем введенные значения
            Fl = self.validate_positive(self.Fl.get(), "Площадь, занятая грузом")
            Vf = self.validate_positive(self.Vf.get(), "Среднее количество грузов")
            if not (Fl and Vf):
                return None
            
            # Получаем значения fobsh1 и fobsh2 из сохраненных атрибутов класса
            if hasattr(self, 'fobsh1') and hasattr(self, 'fobsh2'):
                fobsh1 = self.fobsh1
                fobsh2 = self.fobsh2
            else:
                messagebox.showerror("Ошибка", "Сначала необходимо рассчитать общую площадь склада")
                return None
            
            k_use_space1 = Fl / fobsh1
            k_use_space2 = Fl / fobsh2
            
            k_use_v1 = Vf / sum(self.Vck1)
            k_use_v2 = Vf / sum(self.Vck2)
            
            Qn = float(self.Qn.get())
            Qot = float(self.Qot.get())
            k_ob1 = (Qn + Qot) / (2 * sum(self.Vck1))
            k_ob2 = (Qn + Qot) / (2 * sum(self.Vck2))
            
            T_koef = float(self.T_koef.get())
            self.vg_T = []  # Очищаем список перед заполнением
            for i in range(len(self.V_goods)):
                self.vg_T.append(self.V_goods[i] * self.T[i])
            T_average = sum(self.vg_T) / sum(self.V_goods)
            Qck1 = sum(self.Vck1) * T_koef / T_average
            Qck2 = sum(self.Vck2) * T_koef / T_average
            
            return {
                'k_use_space1': k_use_space1,
                'k_use_space2': k_use_space2,
                'k_use_v1': k_use_v1,
                'k_use_v2': k_use_v2,
                'k_ob1': k_ob1,
                'k_ob2': k_ob2,
                'Qck1': Qck1,
                'Qck2': Qck2
            }
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете коэффициентов: {str(e)}")
            return None

root = tk.Tk()
app = WarehouseCalculator(root)
root.mainloop()

