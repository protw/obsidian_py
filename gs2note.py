import obsidian_util as ou

folders = {
    'base': 'D:/boa_uniteam',
    'vaults_storage': '/OBSIDIAN/',
    'code_dir': 'obsidian-py/',
    'data_dir': 'NECU/'
    }

# Яку таблицю зчитуємо
table = 'persons'

# Встановлюємо повні шляхи до фолдерів коду і даних
code_dir, data_dir = ou.set_dirs(folders)

# Зчитуємо вхідні дані з таблиці Гугл Форми і опис її конвертування до Обсідіан
dfgf, TBL_STRUCT = ou.read_check_gs_table(table, code_dir)

# Перетворення значень стовпчиків зі списку `TBL_STRUCT['pers_name']` з 
# вхідного датафрейму: "Прізвище Ім'я По-батькові" -> "Ім'я Прізвище"
dfgf = ou.pib2ip(dfgf, TBL_STRUCT)

import pandas as pd

# Пряма і зворотня мапи (мітки нотаток Обсідіан) <--> (назви стовпчиків таблиці Гугл Форми)
dfob_cols = TBL_STRUCT['label_refs']
dfob_cols_i = {v: k for k, v in dfob_cols.items()}

dfob = dfgf.copy()
dfob.rename(columns=dfob_cols_i, inplace=True)
if 'title' not in dfob.columns:
    dfob['title'] = dfgf[dfob_cols['title']]
dfob['Позначка часу'] = pd.to_datetime(dfob['Позначка часу'])



#dfob_cols |= TBL_STRUCT['label_vals']

#if TBL_STRUCT['sections']:
