import yaml
import pandas as pd
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
