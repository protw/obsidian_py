import yaml
import pandas as pd
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def set_dirs(folders):
    ''' Встановлюємо повні шляхи до фолдерів коду і даних '''
    # Кореневі дректорії компа
    base = folders['base']
    
    # Конфігурація робочих директорій
    code_dir = base + folders['vaults_storage'] + folders['code_dir']
    data_dir = base + folders['vaults_storage'] + folders['data_dir']
    
    # надання доступу до фолдера коду
    sys.path.insert(0, code_dir)
    
    return code_dir, data_dir


def read_yaml_config(config_file: str='config.yml', 
                     config_gs_file: str='config_gs.yml') -> dict:
    ''' Зчитування конфігураційних словників '''
    with open(config_file) as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    with open(config_gs_file) as f:
        conf_gs = yaml.load(f, Loader=yaml.SafeLoader)
    for k in conf.keys():
        conf[k]['gs_id'] = conf_gs['gs_id'][k]
    conf = {'tables': conf}
    conf['gs_domain'] = conf_gs['gs_domain']
    return conf

def get_gs_table_url(conf: dict, table: str) -> str:
    ''' Створення URL таблиці `table` (Google Sheets) з конфігураційного 
    словника `conf` '''
    tables = list(conf['tables'])
    if table not in tables:
        sys.exit(f'🚩 Таблиця `{table}` відсутня серед таблиць {tables}')
    return conf['gs_domain'] + conf['tables'][table]['gs_id'] + '/edit#gid=0'

def read_gs_by_url(table_url: str, 
                   cred_json_file: str='credentials.json') -> pd.DataFrame:
    ''' Безпечне зчитування таблиці Google Sheets за її URL `table_url` з
    допомогою ключів безпеки Google Cloud з JSON-файлу `cred_json_file` '''
    SCOPES = [
        'https://spreadsheets.google.com/feeds', 
        'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_json_file, SCOPES)
    client = gspread.authorize(creds)

    # Відкриття таблиці за URL
    spreadsheet = client.open_by_url(table_url)
    worksheet = spreadsheet.sheet1

    # Всі дані
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df

''' KEY_LISTS - Функціональні списки назв стовпчиків вх. таблиці Гугл Форми:
  - cols - всі стовпчики, 
  - frontmatter - мітки фронтматерії нотатки Обсідіан, 
  - sections - заголовки розділів нотатки Обсідіан, 
  - not_required - необов'язкові поля Гугл Форми', 
  - pers_name - стовпчики, що потребують перетворення: П.І.Б. -> І.П., 
  - linked - стовпчики, що потребують перетворення: value -> [[value]]
'''
KEY_LISTS = ['cols', 'frontmatter', 'sections', 'not_required', 'pers_name', 'linked']

def check_table_struct(df: pd.DataFrame, TBL_STRUCT: dict) -> list[str]:
    ''' Мінімальна валідація структури вх. таблиці Гугл Форми і словника з 
    описом конвертування цієї таблиці до Обсідіан.
    Вхідні аргументи:
        df - датафрейм вх. таблиці Гугл Форми;
        TBL_STRUCT - описом конвертування вх. таблиці Гугл Форми до Обсідіан.
    Повертає:
        problems - список ключів словника `cond`, де виникли невідповідності 
        (False) ключових елементів `TBL_STRUCT`, `cols`, `df.columns`, 
        `tbl_struct_keys`; якщо все гаразд, то список порожній.
    '''
    def clean_str(lst: str | list[str]) -> str | list[str]:
        ''' Прибирання зайвих пробілів у рядку по краях і всередині  '''
        if isinstance(lst, str):
            lst = ' '.join(lst.split())
        elif isinstance(lst, list):
            lst = [' '.join(s.split()) for s in lst]
        else:
            sys.exit(f'🚩 Або str або list[str]: {lst}')
        return lst
    # Перевіряє чи є `lst` підмножиною `cols`, якщо `lst` порожнє, то повертає True
    check_cols = lambda lst: True if len(lst) == 0 else set(lst).issubset(cols)

    # Прибираємо зайві пробіли у заголовках вх. датафрейму df
    c = clean_str(list(df.columns))
    c_map = {a:b for (a,b) in zip(df.columns, c)}
    df.rename(columns=c_map, inplace=True)
    
    # Прибираємо зайві пробіли у елементах списків `KEY_LISTS` з `TBL_STRUCT`
    for lst in KEY_LISTS:
        TBL_STRUCT[lst] = clean_str(TBL_STRUCT[lst])
    for k, v in TBL_STRUCT['label_refs'].items():
        TBL_STRUCT['label_refs'][k] = clean_str(v)

    # список всіх заголовків вх. таблиці
    cols = set(TBL_STRUCT['cols'])
    # Всі ключі словника `TBL_STRUCT`
    tbl_struct_keys = ['subdir', 'name', 'cols', 'frontmatter', 'sections', 
                       'not_required', 'pers_name', 'linked', 'label_refs', 
                       'label_vals', 'gs_id']
    # Валідація всіх списків
    cond = {
        'tbl_struct_keys': set(TBL_STRUCT.keys()) == set(tbl_struct_keys),
        'df_columns':   cols.issubset(set(df.columns)),
        'frontmatter':  check_cols(TBL_STRUCT['frontmatter']),
        'label_refs':   check_cols(TBL_STRUCT['label_refs'].values()),
        'linked':       check_cols(TBL_STRUCT['linked']),
        'not_required': check_cols(TBL_STRUCT['not_required']),
        'pers_name':    check_cols(TBL_STRUCT['pers_name']),
        'sections':     check_cols(TBL_STRUCT['sections']),
        }
    # Список ключів словника `cond`, де виникли невідповідності (False)
    problems = [k for k, v in cond.items() if not v]
    return problems

def read_check_gs_table(table: str, code_dir: str) -> (pd.DataFrame, dict):
    ''' Зчитує вхідні дані з таблиці Гугл Форми `table` і опис конвертування до 
    Обсідіан. Повертає:
        df - таблиця вхідних даних у вигляді датафрейму
        TBL_STRUCT - опис конвертування до Обсідіан 
    '''
    # Константи алгоритму
    config_file = code_dir + 'config.yml'
    config_gs_file = code_dir + 'config_gs.yml'
    cred_file = code_dir + 'credentials.json'
    
    # Зчитування конфігураційного словника
    conf = read_yaml_config(config_file, config_gs_file)
    # Створення URL таблиці
    table_url = get_gs_table_url(conf, table)
    # Зчитування таблиці Google Sheets за її URL
    df = read_gs_by_url(table_url, cred_file)
    
    if len(df) == 0:
        sys.exit(f'🚩 Таблиця `{table}` порожня!')
    else:
        print(f'✅ Розмір таблиці `{table}` - {df.shape}')
    
    # Опис конвертування вх. таблиці Гугл Форми `table` до Обсідіан
    TBL_STRUCT = conf['tables'][table] # 
    
    # Мінімальна валідація структури таблиці і словника опису конвертування
    problems = check_table_struct(df, TBL_STRUCT)
    
    # Якщо все гаразд, то список `problems` порожній
    if problems:
        sys.exit(f'🚩 Структурні проблеми в таблиці `{table}` такі: {problems}')
    else:
        print(f'✅ Валідація відповідності структури таблиці `{table}` пройдена')

    return df, TBL_STRUCT

def pib2ip(dfgf: pd.DataFrame, TBL_STRUCT: dict) -> pd.DataFrame:
    ''' Перетворення значень стовпчиків зі списку `TBL_STRUCT['pers_name']` з 
    вхідного датафрейму: "Прізвище Ім'я По-батькові" -> "Ім'я Прізвище"
    '''
    for pn in TBL_STRUCT['pers_name']:
        pns = dfgf[pn]
        names = []
        for i, v in pns.items():
            vl = v.split()
            if len(vl) != 3:
                sys.exit(f'🚩 Запис має містити 3 елементи - П.І.Б.: {v}')
            names.append(' '.join([vl[1], vl[0]]))
        dfgf[pn] = names
    return dfgf

