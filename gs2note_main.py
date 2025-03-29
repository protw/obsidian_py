import sys

from gs2note import GS2ON_Convertor

IN_COLAB = 'google.colab' in sys.modules

def run(vault: str='NECU', table: str='persons', 
        folders: dict={}, cond: dict={}):
    if IN_COLAB:
        if not folders:
            folders = {
                'base': '/content/drive',
                'vaults_base': '/MyDrive/OBSIDIAN/',
                'code_dir': 'obsidian-py/',
                'vault_dir': vault + '/'
                }
        from google.colab import drive
        # монтування Гугл Диску
        drive.mount(folders['base'])
    else:
        if not folders:
            folders = {
                'base': 'D:/boa_uniteam/',
                'vaults_base': 'OBSIDIAN/',
                'code_dir': 'obsidian-py/',
                'vault_dir': vault + '/'
                }

    if not cond:
        cond = {
            'is_dupl_in_vault': True, # Рекомендовано True, за замовчанням
            'is_dupl_in_table': True,  # Рекомендовано True, за замовчанням
            ## ---- СХОВАТИ ВІД КОРИСТУВАЧА ----
            'not_write_dupl':   True,  # Рекомендовано True, за замовчанням
            'is_clean_writing': True  # За замовчанням True
            }

    # Ініціюємо конвертор. Встановлюємо повні шляхи до фолдерів коду і даних
    conv = GS2ON_Convertor(folders, **cond)
    
    # Основоний метод класу `GS2ON_Convertor`
    conv.main(table)
    
    return conv

if __name__ == '__main__':
    cond = {
        'is_dupl_in_vault': False, # Рекомендовано True, за замовчанням
        'is_dupl_in_table': True,  # Рекомендовано True, за замовчанням
        ## ---- СХОВАТИ ВІД КОРИСТУВАЧА ----
        'not_write_dupl':   False,  # Рекомендовано True, за замовчанням
        'is_clean_writing': False  # За замовчанням True
        }
    # Визначаємо сховище
    vault = 'NECU'
    # Яку таблицю зчитуємо
    table = 'persons'
    
    conv = run(vault=vault, table=table, cond=cond)
    
