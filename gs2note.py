import obsidian_util as ou

# Константи алгоритму
config_file = 'config.yml'
cred_file = 'credentials.json'

# Яку таблицю зчитуємо
table = 'persons'
# Зчитування конфігураційного словника
conf = ou.read_yaml_config(config_file)
# Створення URL таблиці
table_url = ou.get_gs_table_url(conf, table)
# Зчитування таблиці Google Sheets за її URL
df = ou.read_gs_by_url(table_url, cred_file)

print(df)