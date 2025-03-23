import sys

def set_dirs(folders):
    # Кореневі дректорії компа
    base = folders['base']
    
    # Конфігурація робочих директорій
    code_dir = base + folders['vaults_storage'] + folders['code_dir']
    data_dir = base + folders['vaults_storage'] + folders['data_dir']
    
    # надання доступу до фолдера коду
    sys.path.insert(0, code_dir)
    
    return code_dir, data_dir


import obsidian_util as ou

folders = {
    'base': 'D:/boa_uniteam',
    'vaults_storage': '/OBSIDIAN/',
    'code_dir': 'obsidian-py/',
    'data_dir': 'NECU/'
    }

code_dir, data_dir = set_dirs(folders)

# Константи алгоритму
config_file = code_dir + 'config.yml'
config_gs_file = code_dir + 'config_gs.yml'
cred_file = code_dir + 'credentials.json'

# Яку таблицю зчитуємо
table = 'persons'
# Зчитування конфігураційного словника
conf = ou.read_yaml_config(config_file, config_gs_file)
# Створення URL таблиці
table_url = ou.get_gs_table_url(conf, table)
# Зчитування таблиці Google Sheets за її URL
df = ou.read_gs_by_url(table_url, cred_file)

print(df)
