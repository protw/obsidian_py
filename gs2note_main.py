import sys

from gs2note import GS2ON_Convertor

IN_COLAB = 'google.colab' in sys.modules

def run(vault: str, table: str, folders: dict, cond: dict) -> GS2ON_Convertor:
    if IN_COLAB:
        from google.colab import drive
        # монтування Гугл Диску
        drive.mount(folders['base'])

    # Ініціюємо конвертор. Встановлюємо повні шляхи до фолдерів коду і даних
    conv = GS2ON_Convertor(folders, **cond)
    
    print('ВХІДНІ ПАРАМЕТРИ\n'
          f'✅ Фолдер Обсідіан-сховища: {conv.vault_dir}\n'
          f'✅ Фолдер налаштувань: {conv.code_dir}\n'
          f'✅ Тип конвертованої таблиці: {table}\n'
          'ЗАПУСК КОНВЕРТОРА')
    
    # Основоний метод класу `GS2ON_Convertor`
    conv.main(table)
    
    return conv

if __name__ == '__main__':
    # ==== ВХІДНІ ПАРАМЕТРИ ====

    # Оберіть Обсідіан-сховище (vault):
    vault = 'NECU' # обрати зі списку ['NECU', 'NCP-NEB']

    # Оберіть тип таблиці (table), що буде конвертований з Гугл форми
    # до обраного сховища:
    table = 'persons' # обрати зі списку ['persons', 'teams', 'orgs', 'proj']

    # ==== УВАГА! Цей розділ лише для адміна!! ====

    # Якщо ви не знаєте призначення налаштувань нижче, або не впевнені в тому
    # що знаєте, то нічого не чипайте
    folders = {
        'base': 'D:/boa_uniteam/',
        'vaults_base': 'OBSIDIAN/',
        'code_dir': 'obsidian-py/',
        'vault_dir': vault + '/'
    }
    # В робочому положенні ВСІ елементи словника `cond` мають бут встановлені `True`
    cond = {
        'is_dupl_in_vault': False, # Рекомендовано True, за замовчанням
        'is_dupl_in_table': True,  # Рекомендовано True, за замовчанням
        ## ---- СХОВАТИ ВІД КОРИСТУВАЧА ----
        'not_write_dupl':   False,  # Рекомендовано True, за замовчанням
        'is_clean_writing': False  # За замовчанням True
    }

    conv = run(vault=vault, table=table, folders=folders, cond=cond)
    
