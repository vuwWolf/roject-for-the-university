# Константы
kckmin = 0.8
kckmax = 0.9
knmin = 1.1
knmax = 1.5

def parse_float(value):
    """Преобразует строку с числом в float, поддерживая и запятую, и точку как разделитель"""
    try:
        # Заменяем запятую на точку
        value = value.replace(',', '.')
        return float(value)
    except ValueError:
        return None

# Листы для ввода переменных
qcr = []
vg_T = []
V_goods = []
T = []
Vck1 = []
Vck2 = []
h = []
y = []
p = []
kpi = []
Fck1 = []
Fck2 = []
Qci = []
Fnc1 = []
Fnc2 = []

# Ввод данных для расчётов
while True:
    try:
        a = int(input('Введите количество поступающих на склад грузов: '))
        if a > 0:
            break
        print('Количество грузов должно быть положительным числом. Попробуйте снова.')
    except ValueError:
        print('Введите целое число. Попробуйте снова.')

# Ввод qcr
for i in range(a):
    while True:
        try:
            element = parse_float(input(f'Введите расчётный суточный грузопоток для груза {i + 1} (в тоннах):  '))
            if element is not None and element > 0:
                break
            print('Грузопоток должен быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    qcr.append(element)

# Ввод T
for i in range(a):
    while True:
        try:
            element = parse_float(input(f'Срок хранения для поступившего для груза {i + 1} (в сутках): '))
            if element is not None and element > 0:
                break
            print('Срок хранения должен быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    T.append(element)

# Выбор pi
print(f'Выберите значение удельной нагрузки для каждого груза:\n'
          f'1 - (0,85) для крытых складов и платформ общего назначения и при хранении тарных и штучных грузов, перевозимых повагонными отправками;\n'
          f'2 - (0,40) для складов тарно-штучных грузов, перевозимых мелкими отправками;\n'
          f'3 - (0,25) для специализированных складов промышленных товаров широкого потребления (трикотаж, обувь, одежда и т.п.);\n'
          f'4 - (0,50) для контейнерных площадок;\n'
          f'5 - (0,90) для площадок тяжеловесных грузов;\n'
          f'6 - (1,10) для площадок навалочных грузов.\n')
for i in range(a):
    while True:
        element = parse_float(input(f'Введите значение удельной нагрузки для {i + 1}: '))
        if element == 1:
            p.append(0.85)
            break
        elif element == 2:
            p.append(0.40)
            break
        elif element == 3:
            p.append(0.25)
            break
        elif element == 4:
            p.append(0.50)
            break
        elif element == 5:
            p.append(0.90)
            break
        elif element == 6:
            p.append(1.10)
            break
        else:
            print('Выберите число от 1 до 6. Попробуйте снова.')

while True:
    try:
        width = parse_float(input('Введите ширину вашего склада (в метрах): '))
        if width is not None and width > 0:
            break
        print('Ширина склада должна быть положительным числом. Попробуйте снова.')
    except ValueError:
        print('Введите число. Попробуйте снова.')

print('Укажите тип грузов: \n'
      '1 - однородные крупногабаритные груза;\n'
      '2 - мелкопартионные груза.')
while True:
    goodstype = int(input())
    if goodstype in [1, 2]:
        break
    print('Выберите 1 или 2. Попробуйте снова.')

if width < 24:
    if goodstype == 1: kip = 0.65
    elif goodstype == 2: kip = 0.55
elif width >= 24 and width < 30:
    if goodstype == 1: kip = 0.7
    elif goodstype == 2: kip = 0.6
elif width >= 30:
    if goodstype == 1: kip = 0.75
    elif goodstype == 2: kip = 0.65

# Расчёт вместимости склада
def f_vck():
    # Вывод Вместимости склада (Vck)
    for i in range(a):
    # Расчёт элементов Vck с коэффициентом складируемости 0.8
        element = kckmin * qcr[i] * T[i]
        Vck1.append(element)
    for i in range(a):
    # Расчёт элементов Vck с коэффициентом складируемости 0.9
        element = kckmax * qcr[i] * T[i]
        Vck2.append(element)
    print(f'Вместимость склада при коэффициенте складируемости 0,8: {sum(Vck1)}\n'
          f'Вместимость склада при коэффициенте складируемости 0,9: {sum(Vck2)}')
    return Vck1, Vck2

# Ориентировочный расчёт площади склада
def f_Fck():
    # Выбор kpi - коэффициента, учитывающего площадь складских проездов
    print(f'Выберите коэффициент, учитывающий площадь складских проездов, для каждого груза: \n'
          f'1,7 - для крытых складов и платформ при хранении тарных и штучных грузов, перевозимых повагонными отправками; \n'
          f'2,0 - мелкими отправками;\n'
          f'1,9 - для контейнерных площадок;\n'
          f'1,6 - для площадок тяжеловесных грузов и лесоматериалов;\n'
          f'1,5 - для складов угля и минерально-строительных материалов (щебень, гравий, песок).\n')
    for i in range(a):
        while True:
            element = parse_float(input(f'Введите значение коэффицента для {i + 1} груза: '))
            if element > 0:
                break
            print('Коэффициент должен быть положительным числом. Попробуйте снова.')
        kpi.append(element)
    # Расчёт ориентировачной площади склада
    for i in range(a):
        element = kpi[i] * ((kckmin * qcr[i] * T[i]) / p[i])
        Fck1.append(element)
        element = kpi[i] * ((kckmax * qcr[i] * T[i]) / p[i])
        Fck2.append(element)
    print(f'Ориентировачная площадь склада при коэф. складируемости 0.8: {sum(Fck1)}')
    print(f'Ориентировачная площадь склада при коэф. складируемости 0.9: {sum(Fck2)}')

# Расчёт площади приёмо-сортировочных, комплектовочных площадок складов промышленных предприятий
def f_Fnc():
    for i in range(a):
        while True:
            element = parse_float(input(f'Введите среднесуточное поступление или отпуск материала для груза {i + 1 } в (в т/сут): '))
            if element > 0:
                break
            print('Значение должно быть положительным числом. Попробуйте снова.')
        Qci.append(element)
    for i in range(a):
        element = (knmin * Qci[i] * T[i]) / p[i]
        Fnc1.append(element)
        element = (kckmax * Qci[i] * T[i]) / p[i]
        Fnc2.append(element)
    print(f'Площадь приёмо-сортировочных, комплектовочных площадок складов промышленных предприятий при коэф. складируемости 0.8: {sum(Fnc1)}')
    print(f'Площадь приёмо-сортировочных, комплектовочных площадок складов промышленных предприятий при коэф. складируемости 0.9: {sum(Fnc2)}')

# Расчёт полезной площади склада
def f_Fpol():
    Vck1, Vck2 = f_vck()
    while True:
        try:
            P = parse_float(input('Введите расчётную эксплуатационную нагрузку на 1 кв.м. полезной площади склада (в тоннах): '))
            if P is not None and P > 0:
                break
            print('Нагрузка должна быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    Fpol1 = sum(Vck1) / (kip * P)
    Fpol2 = sum(Vck2) / (kip * P)
    print(f'Полезная площадь склада при коэф. складируемости 0.8: {Fpol1}')
    print(f'Полезная площадь склада при коэф. складируемости 0.9: {Fpol2}')
    return kip

# Расчёт общей площади склада
def f_Fobsh():
    kip = f_Fpol()
    while True:
        try:
            dV = parse_float(input(f'Введите вместимость одного штабеля/стеллажа: '))
            if dV is not None and dV > 0:
                break
            print('Вместимость должна быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    Vck1, Vck2 = f_vck()
    nl1 = sum(Vck1) / dV
    nl2 = sum(Vck2) / dV
    while True:
        try:
            L = parse_float(input('Введите длину одного штабеля (в метрах): '))
            if L is not None and L > 0:
                break
            print('Длина должна быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    while True:
        try:
            W = parse_float(input('Введите ширину одного штабеля (в метрах): '))
            if W is not None and W > 0:
                break
            print('Ширина должна быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    deltaF = L * W * kip
    fobsh1 = nl1 * deltaF
    fobsh2 = nl2 * deltaF
    return fobsh1, fobsh2

# Расчёт коэффицентов
def f_koef():
    # Коэффициент использования площади склада
    fobsh1, fobsh2 = f_Fobsh()
    while True:
        try:
            Fl = parse_float(input('Введите площадь непосредственно занятую грузом (в кв.м): '))
            if Fl is not None and Fl > 0:
                break
            print('Площадь должна быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    k_use_space1 = Fl / fobsh1
    k_use_space2 = Fl / fobsh2
    print(f'Коэффициент использования площади склада при коэф. складируемости 0.8: {k_use_space1}')
    print(f'Коэффициент использования площади склада при коэф. складируемости 0.9: {k_use_space2}')
    
    # Коэффициент использования склада по вместимости
    Vck1, Vck2 = f_vck()
    while True:
        try:
            Vf = parse_float(input('Введите среднее количества грузов на складе за определённый период времени (в тоннах): '))
            if Vf is not None and Vf > 0:
                break
            print('Количество грузов должно быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    k_use_v1 = Vf / sum(Vck1)
    k_use_v2 = Vf / sum(Vck2)
    print(f'Коэффициент использования склада по вместимости при коэф. складируемости 0.8: {k_use_v1}')
    print(f'Коэффициент использования склада по вместимости при коэф. складируемости 0.9: {k_use_v2}')

    # Коэффициент оборота склада
    while True:
        try:
            Qn = parse_float(input('Введите поступление грузов на склад (в тоннах): '))
            if Qn is not None and Qn > 0:
                break
            print('Поступление грузов должно быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    while True:
        try:
            Qot = parse_float(input('Введите отпуск грузов со склада (в тоннах): '))
            if Qot is not None and Qot > 0:
                break
            print('Отпуск грузов должен быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    k_ob1 = (Qn + Qot) / (2 * sum(Vck1))
    k_ob2 = (Qn + Qot) / (2 * sum(Vck2))
    print(f'Коэффициент оборота склада при коэф. складируемости 0.8: {k_ob1}')
    print(f'Коэффициент оборота склада при коэф. складируемости 0.9: {k_ob2}')
    
    # Коэффициент использования склада по грузопереработке
    while True:
        try:
            T_koef = parse_float(input('Укажите период времени за который будет пропущено определённое количество грузов (в сутках): '))
            if T_koef is not None and T_koef > 0:
                break
            print('Период времени должен быть положительным числом. Попробуйте снова.')
        except ValueError:
            print('Введите число. Попробуйте снова.')
    for i in range(a):
        while True:
            try:
                element = parse_float(input(f'Введите объём груза {i + 1} (в тоннах): '))
                if element is not None and element > 0:
                    break
                print('Объём груза должен быть положительным числом. Попробуйте снова.')
            except ValueError:
                print('Введите число. Попробуйте снова.')
        V_goods.append(element)
    for i in range(a):
        vg_T.append(V_goods[i] * T[i])
    T_average = sum(vg_T) / sum(V_goods)
    Qck1 = sum(Vck1) * T_koef / T_average
    Qck2 = sum(Vck2) * T_koef / T_average
    print(f'Коэффициент использования склада по грузопереработке при коэф. складируемости 0.8: {Qck1}')
    print(f'Коэффициент использования склада по грузопереработке при коэф. складируемости 0.9: {Qck2}')
f_koef()
