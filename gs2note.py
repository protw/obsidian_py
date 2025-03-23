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

# Зчитуємо вхідні дані з таблиці Гугл Форми і опис конвертування до Обсідіан
dfgf, TBL_STRUCT = ou.read_check_gs_table(table, code_dir)

import pandas as pd

dfob_cols = {'title': TBL_STRUCT['title']} | TBL_STRUCT['label_refs'] 
dfob_cols_i = {v: k for k, v in dfob_cols.items()}

dfob = dfgf.copy()
dfob.rename(columns=dfob_cols_i, inplace=True)
dfob['Позначка часу'] = pd.to_datetime(dfob['Позначка часу'])


#dfob_cols |= TBL_STRUCT['label_vals']

#if TBL_STRUCT['sections']:
