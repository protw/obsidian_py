import pandas as pd

import obsidian_util as ou

folders = {
    'base': 'D:/boa_uniteam',
    'vaults_storage': '/OBSIDIAN/',
    'code_dir': 'obsidian-py/',
    'data_dir': 'NECU/'
    }

# Яку таблицю зчитуємо
table = 'teams'

# Встановлюємо повні шляхи до фолдерів коду і даних
code_dir, data_dir = ou.set_dirs(folders)

# Зчитуємо вхідні дані з таблиці Гугл Форми і опис її конвертування до Обсідіан
dfgf, TBL_STRUCT = ou.read_check_gs_table(table, code_dir)

# Перетворення значень стовпчиків зі списку `TBL_STRUCT['pers_name']` з 
# вхідного датафрейму: "Прізвище Ім'я По-батькові" -> "Ім'я Прізвище"
dfgf = ou.pib2ip(dfgf, TBL_STRUCT)

# Перетворення значень стовпчиків зі списку `TBL_STRUCT['linked']` з 
# вхідного датафрейму у внутрішнє Обсідіан-посилання: name -> [[name]]
dfgf = ou.make_linked(dfgf, TBL_STRUCT)

# Копія таблиці зі скороченими назвами стовпчиків
dfob, dfob_cols = ou.dfgf2dfob(dfgf, TBL_STRUCT)

# Перевірка відсутності дублікатів імен нотаток
ou.check_duplicates(dfob, dfgf, table, dfob_cols)

#dfob_cols['title']
dfob['Позначка часу'] = pd.to_datetime(dfob['Позначка часу'])



#dfob_cols |= TBL_STRUCT['label_vals']

#if TBL_STRUCT['sections']:
