import sys

from gs2note import GS2ON_Convertor

IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    folders = {
        'base': '/content/drive',
        'vaults_base': '/MyDrive/OBSIDIAN/',
        'code_dir': 'obsidian-py/',
        'vault_dir': 'NECU/'
        }
    from google.colab import drive
    # монтування Гугл Диску
    drive.mount(folders['base'])
else:
    folders = {
        'base': 'D:/boa_uniteam/',
        'vaults_base': 'OBSIDIAN/',
        'code_dir': 'obsidian-py/',
        'vault_dir': 'NECU/'
        }

cond = {
    'is_dupl_in_vault': False, # Рекомендовано True, за замовчанням
    'is_dupl_in_table': True,  # Рекомендовано True, за замовчанням
    ## ---- СХОВАТИ ВІД КОРИСТУВАЧА ----
    'not_write_dupl':   False,  # Рекомендовано True, за замовчанням
    'is_clean_writing': False  # За замовчанням True
    }

# Яку таблицю зчитуємо
table = 'persons'

# Ініціюємо конвертор. Встановлюємо повні шляхи до фолдерів коду і даних
conv = GS2ON_Convertor(folders, **cond)

# Основоний метод класу `GS2ON_Convertor`
conv.main(table)
