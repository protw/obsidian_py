import pandas as pd

from obsidian_util_cl import GS2ON_Convertor

folders = {
    'base': 'D:/boa_uniteam',
    'vaults_storage': '/OBSIDIAN/',
    'code_dir': 'obsidian-py/',
    'data_dir': 'NECU/'
    }

# Яку таблицю зчитуємо
table = 'persons'

# Ініціюємо конвертор. Встановлюємо повні шляхи до фолдерів коду і даних
conv = GS2ON_Convertor(folders)

# Зчитуємо вхідні дані з таблиці Гугл Форми і опис її конвертування до Обсідіан
conv.read_gs_table(table)

# Валідація структури вх. таблиці Гугл Форми і словника з описом конвертування 
# цієї таблиці до Обсідіан
conv.check_table_struct()

# Перетворення значень стовпчиків зі списку `TBL_STRUCT['pers_name']` з 
# вхідного датафрейму: "Прізвище Ім'я По-батькові" -> "Ім'я Прізвище"
conv.pib2ip()

# Перетворення значень стовпчиків зі списку `TBL_STRUCT['linked']` з 
# вхідного датафрейму у внутрішнє Обсідіан-посилання: name -> [[name]]
conv.make_linked()

# Копія таблиці зі скороченими назвами стовпчиків
conv.dfgf2dfob()

# Перевірка відсутності дублікатів імен нотаток
conv.check_duplicates()

#dfob_cols['title']
conv.dfob['Позначка часу'] = pd.to_datetime(conv.dfob['Позначка часу'])



