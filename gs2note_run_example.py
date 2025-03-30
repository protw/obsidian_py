''' Запуск конвертора GS2NOTE на локальном комп'ютері '''

import gs2note

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
    'base': 'D:/PATH_FOR_VAULTS_AND_CONFIG/',
    'vaults_base': 'OBSIDIAN/',
    'code_dir': 'obsidian-py/'
}
# В робочому положенні ВСІ елементи словника `cond` мають бут встановлені `True`
cond = {
    'is_dupl_in_vault': False, # Рекомендовано True, за замовчанням
    'is_dupl_in_table': True,  # Рекомендовано True, за замовчанням
    'not_write_dupl':   False,  # Рекомендовано True, за замовчанням
    'is_clean_writing': False  # За замовчанням True
}

conv = gs2note.run(vault=vault, table=table, folders=folders, cond=cond)

