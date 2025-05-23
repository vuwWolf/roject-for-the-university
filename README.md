# Калькулятор параметров склада

Веб-приложение для расчета параметров склада.

## Онлайн версия

Приложение доступно онлайн по адресу: [https://vuwwolf.github.io/roject-for-the-university/](https://vuwwolf.github.io/roject-for-the-university/)

## Структура проекта

```
├── Python/                 # Исходная Python версия
│   ├── main.py            # Основной файл с логикой расчетов
│   ├── ui.py              # Файл с пользовательским интерфейсом
│   └── test.spec          # Спецификация для сборки
├── index.html             # Основная страница с формой ввода
├── styles.css             # Стили оформления
├── warehouseCalculator.js # JavaScript код с логикой расчетов
├── LICENSE               # Лицензия проекта
└── README.md            # Этот файл
```

## Как использовать

### Онлайн версия
1. Перейдите на [сайт приложения](https://vuwwolf.github.io/roject-for-the-university/)
2. Заполните форму и нажмите "Рассчитать"

### Локальная версия
1. Откройте файл `web/index.html` в любом современном веб-браузере
2. Заполните форму:
   - Введите количество грузов
   - Для каждого груза укажите:
     - Расчётный суточный грузопоток (в тоннах)
     - Срок хранения (в сутках)
     - Удельную нагрузку (выберите из списка)
   - Укажите ширину склада (в метрах)
   - Выберите тип грузов
3. Нажмите кнопку "Рассчитать"
4. Результаты расчетов появятся под формой

## Требования

- Современный веб-браузер с поддержкой JavaScript
- Не требуется установка дополнительного ПО

## Примечания

- Все числовые значения должны быть положительными
- Для десятичных чисел используйте точку или запятую
- Результаты округляются до двух знаков после запятой 