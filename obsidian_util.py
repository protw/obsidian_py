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
        sys.exit(f'Таблиця `{table}` відсутня серед таблиць {tables}')
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

def check_table_struct(conf: dict, table: str, df: pd.DataFrame) -> (dict, dict):
    ''' Мінімальна валідація відповідності структури таблиці і конфігураційного 
    словника '''
    def clean_str(lst):
        if isinstance(lst, str):
            lst = ' '.join(lst.split())
        elif isinstance(lst, list):
            lst = [' '.join(s.split()) for s in lst] if len(lst) > 0 else []
        else:
            sys.exit(f'Або str або list[str]: {lst}')
        return lst
    check_cols = lambda lst: True if len(lst) == 0 else set(lst).issubset(cols)

    # Прибираємо зайві пробіли у заголовках вхідної таблиці
    c = clean_str(list(df.columns))
    c_map = {a:b for (a,b) in zip(df.columns, c)}
    df.rename(columns=c_map, inplace=True)
    
    TBL_STRUCT = conf['tables'][table]
    
    lsts = ['cols', 'title', 'frontmatter', 'sections', 'not_required', 
            'pers_name', 'linked']
    for lst in lsts:
        TBL_STRUCT[lst] = clean_str(TBL_STRUCT[lst])
    for k, v in TBL_STRUCT['label_refs'].items():
        TBL_STRUCT['label_refs'][k] = clean_str(v)

    cols = set(TBL_STRUCT['cols'])
    tbl_struct_keys = ['subdir', 'name', 'cols', 'title', 'frontmatter', 
                       'sections', 'not_required', 'pers_name', 'linked', 
                       'label_refs', 'label_vals', 'gs_id']
    cond = {
        'tbl_struct_keys': set(TBL_STRUCT.keys()) == set(tbl_struct_keys),
        'df_columns':   cols.issubset(set(df.columns)),
        'frontmatter':  check_cols(TBL_STRUCT['frontmatter']),
        'label_refs':   check_cols(TBL_STRUCT['label_refs'].values()),
        'linked':       check_cols(TBL_STRUCT['linked']),
        'not_required': check_cols(TBL_STRUCT['not_required']),
        'pers_name':    check_cols(TBL_STRUCT['pers_name']),
        'sections':     check_cols(TBL_STRUCT['sections']),
        'title':        check_cols([TBL_STRUCT['title']]),
        }
    problems = [k for k, v in cond.items() if not v]
    return problems, TBL_STRUCT

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
        sys.exit(f'Таблиця `{table}` порожня!')
    else:
        print(f'Розмір таблиці `{table}` - {df.shape}')
    
    # Мінімальна валідація відповідності структури таблиці і конфігураційного словника
    problems, TBL_STRUCT = check_table_struct(conf, table, df)
    
    if problems:
        sys.exit(f'Структурні проблеми в таблиці `{table}` такі: {problems}')
    else:
        print(f'Валідація відповідності структури таблиці `{table}` пройдена')

    return df, TBL_STRUCT

