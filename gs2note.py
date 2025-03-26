from pathlib import Path
import yaml
import pandas as pd
import sys
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GS2ON_Convertor():
    ''' Google Sheets to Obsidian notes convertor '''

    ''' KEY_LISTS - Функціональні списки назв стовпчиків вх. таблиці Гугл Форми:
    - cols - всі стовпчики, 
    - frontmatter - мітки фронтматерії нотатки Обсідіан, 
    - sections - заголовки розділів нотатки Обсідіан, 
    - not_required - необов'язкові поля Гугл Форми', 
    - pers_name - стовпчики, що потребують перетворення: П.І.Б. -> І.П., 
    - linked - стовпчики, що потребують перетворення: value -> [[value]]
    '''
    KEY_LISTS = ['cols', 'frontmatter', 'sections', 'not_required', 'pers_name', 
                 'linked']
    # Всі ключі словника `TBL_STRUCT`
    tbl_struct_keys = ['subdir', 'name', 'cols', 'frontmatter', 'sections', 
                       'not_required', 'pers_name', 'linked', 'label_refs', 
                       'label_vals', 'gs_id']

    def __init__(self, folders: dict, is_dupl_in_vault: bool=True, 
                 is_dupl_in_table: bool=True, not_write_dupl: bool=True,
                 is_clean_writing: bool=True):
        ''' Встановлюємо повні шляхи до фолдерів коду і даних '''
        # Кореневі дректорії компа
        base = folders['drive_base']
        self.vault = folders['vault_dir']
        
        # Конфігурація робочих директорій
        self.code_dir = base + folders['vaults_base'] + folders['code_dir']
        self.vault_dir = base + folders['vaults_base'] + self.vault
        
        # Умови запуску
        self.is_dupl_in_vault = is_dupl_in_vault
        self.is_dupl_in_table = is_dupl_in_table
        self.not_write_dupl = not_write_dupl
        self.is_clean_writing = is_clean_writing

        # Перевірка дублікатів назв нотаток у сховищі Обсідіан
        self.check_dupl_in_vault()
        
        # надання доступу до фолдера коду
        sys.path.insert(0, self.code_dir)
        
        # Константи алгоритму
        self.config_file = self.code_dir + 'config.yml'
        self.config_gs_file = self.code_dir + 'config_gs.yml'
        self.cred_file = self.code_dir + 'credentials.json'
        
        # Створення конфігураційного словника self.conf
        self.read_yaml_config()

    def check_dupl_in_vault(self):
        ''' Перевірка дублікатів назв нотаток у сховищі Обсідіан '''
        def get_all_filenames(root_folder):
            ''' Отримує список усіх назв файлів у сховищі Obsidian '''
            filenames = []
            for file in root_folder.rglob("*.*"):
                # Перевіряємо, чи є приховані папки в шляху, що починаються з крапки '.'
                if any(part.startswith('.') for part in file.parts):
                    continue
                filenames.append(file.name)  # Без розширення
            return pd.Series(filenames)

        all_notes = get_all_filenames(Path(self.vault_dir))
        dupl_names = set(all_notes.loc[all_notes.duplicated(keep='first')])
        excl_names = {'desktop.ini'} # Список імен файлів на виключення
        dupl_names -= excl_names # Виключаємо файли згідно списку

        if len(dupl_names) > 0:
            print(f'❗ У сховищі {self.vault} дублювання назв {len(dupl_names)} '
                  f'нотаток: {dupl_names}')
            if self.is_dupl_in_vault:
                sys.exit('🚩 Усуньте дублювання і повторіть спробу!')

        self.all_notes = all_notes.loc[~all_notes.duplicated(keep='first')]

    def read_yaml_config(self):
        ''' Зчитування конфігураційних словників з файлів і створення 
        внутрішнього конфігураційного словника '''
        with open(self.config_file) as f:
            conf = yaml.load(f, Loader=yaml.SafeLoader)
        with open(self.config_gs_file) as f:
            conf_gs = yaml.load(f, Loader=yaml.SafeLoader)
        for k in conf.keys():
            conf[k]['gs_id'] = conf_gs['gs_id'][k]
        conf = {'tables': conf}
        conf['gs_domain'] = conf_gs['gs_domain']
        self.conf = conf

    def read_gs_table(self, table):
        ''' Встановлюємо тип таблиці, що визначений у conf['tables'].
        Попередньо має бути виконаний метод read_yaml_config. '''
        ''' Безпечне зчитування таблиці Google Sheets за її URL `table_url` з
        допомогою ключів безпеки Google Cloud з JSON-файлу `cred_file` '''

        tables = list(self.conf['tables'])
        if table not in tables:
            sys.exit(f'🚩 Таблиця {table.upper()} відсутня серед таблиць {tables}')

        # Опис конвертування вх. таблиці Гугл Форми `table` до Обсідіан
        self.TBL_STRUCT = self.conf['tables'][table]

        # Зчитування таблиці Google Sheets за її URL, створення датафрейму self.dfgf

        # Створення URL таблиці self.table_url
        self.table_url = self.conf['gs_domain'] + \
            self.conf['tables'][table]['gs_id'] + '/edit#gid=0'

        SCOPES = [
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_file, SCOPES)
        client = gspread.authorize(creds)

        # Відкриття таблиці за URL
        spreadsheet = client.open_by_url(self.table_url)
        worksheet = spreadsheet.sheet1

        # Всі дані
        data = worksheet.get_all_records()
        self.dfgf = pd.DataFrame(data)

        if len(self.dfgf) == 0:
            sys.exit(f'🚩 Таблиця {table.upper()} порожня!')
        else:
            print(f'✅ Зчитана таблиця {table.upper()} розміром {self.dfgf.shape}')

        self.table = table

    def check_table_struct(self):
        ''' Мінімальна валідація структури вх. таблиці Гугл Форми і словника з 
        описом конвертування цієї таблиці до Обсідіан.
        Вхідні аргументи:
            dfgf - датафрейм вх. таблиці Гугл Форми;
            TBL_STRUCT - описом конвертування вх. таблиці Гугл Форми до Обсідіан.
        Повертає:
            problems - список ключів словника `cond`, де виникли невідповідності 
            (False) ключових елементів `TBL_STRUCT`, `cols`, `dfgf.columns`, 
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

        # Прибираємо зайві пробіли у заголовках вх. датафрейму dfgf
        c = clean_str(list(self.dfgf.columns))
        c_map = {a:b for (a,b) in zip(self.dfgf.columns, c)}
        self.dfgf.rename(columns=c_map, inplace=True)

        # Прибираємо зайві пробіли у елементах списків `KEY_LISTS` з `TBL_STRUCT`
        for lst in self.KEY_LISTS:
            self.TBL_STRUCT[lst] = clean_str(self.TBL_STRUCT[lst])
        for k, v in self.TBL_STRUCT['label_refs'].items():
            self.TBL_STRUCT['label_refs'][k] = clean_str(v)

        # список всіх заголовків вх. таблиці
        cols = set(self.TBL_STRUCT['cols'])
        # Валідація всіх списків
        cond = {
            'tbl_struct_keys': set(self.TBL_STRUCT.keys()) == set(self.tbl_struct_keys),
            'df_columns':   cols.issubset(set(self.dfgf.columns)),
            'frontmatter':  check_cols(self.TBL_STRUCT['frontmatter']),
            'label_refs':   check_cols(self.TBL_STRUCT['label_refs'].values()),
            'linked':       check_cols(self.TBL_STRUCT['linked']),
            'not_required': check_cols(self.TBL_STRUCT['not_required']),
            'pers_name':    check_cols(self.TBL_STRUCT['pers_name']),
            'sections':     check_cols(self.TBL_STRUCT['sections']),
            }
        # Список ключів словника `cond`, де виникли невідповідності (False)
        problems = [k for k, v in cond.items() if not v]
    
        # Якщо все гаразд, то список `problems` порожній
        if problems:
            sys.exit(f'🚩 Структурні проблеми в таблиці `{self.table.upper()}` '
                     f'такі: {problems}')
        else:
            print('✅ Валідація відповідності структури таблиці '
                  f'`{self.table.upper()}` пройдена')

    def pib2ip(self):
        ''' Перетворення значень стовпчиків зі списку `TBL_STRUCT['pers_name']` з 
        вхідного датафрейму: "Прізвище Ім'я По-батькові" -> "Ім'я Прізвище"
        '''
        for pn in self.TBL_STRUCT['pers_name']:
            pns = self.dfgf[pn]
            names = []
            for i, v in pns.items():
                vl = v.split()
                if len(vl) != 3:
                    sys.exit(f'🚩 Запис має містити 3 елементи - П.І.Б.: {v}')
                names.append(' '.join([vl[1], vl[0]]))
            self.dfgf[pn] = names

    def make_linked(self):
        ''' Перетворення значень стовпчиків зі списку `TBL_STRUCT['linked']` з 
        вхідного датафрейму у внутрішнє Обсідіан-посилання: name -> [[name]] 
        '''
        for name in self.TBL_STRUCT['linked']:
            linked_names = ['"[[' + s + ']]"' for _, s in self.dfgf[name].items()]
            self.dfgf[name] = linked_names

    def dfgf2dfob(self):
        ''' Копія таблиці зі скороченими назвами стовпчиків - назви міток 
        фронтматерії. Таблиця готується для формування нотаток Обсідіан.
        '''
        # Пряма і зворотня мапи:
        # (мітки нотаток Обсідіан) <--> (назви стовпчиків таблиці Гугл Форми)
        dfob_cols = self.TBL_STRUCT['label_refs']
        dfob_cols_i = {v: k for k, v in dfob_cols.items()}
    
        dfob = self.dfgf.copy()
        dfob.rename(columns=dfob_cols_i, inplace=True)
        if 'title' not in dfob.columns:
            dfob['title'] = self.dfgf[dfob_cols['title']]

        self.dfob_cols = dfob_cols
        self.dfob = dfob

    def check_dupl_in_table(self):
        ''' Перевірка відсутності дублікатів імен нотаток у вх. таблиці '''
        idx_dfob_dupl = self.dfob.duplicated(subset='title', keep=False)
        dfgf_dupl = self.dfgf.loc[idx_dfob_dupl]
        if len(dfgf_dupl) > 0:
            print(f'❗ У вхідній таблиці {self.table.upper()} виявлені '
                  'дублікати назв нотаток:')
            print(self.dfgf[self.dfob_cols['title']].to_markdown())
            if self.is_dupl_in_table:
                sys.exit('🚩 Усуньте дублікати і повторіть спробу.')

    def complete_obs_table(self):
        ''' Завершення підготовки Обсідіан таблиці перед конвертацією у нотатки '''
        self.dfob['Позначка часу'] = pd.to_datetime(self.dfob['Позначка часу'])

        # Дадаємо стовпчики 'label_vals' з постійними значеннями
        for k, v in self.TBL_STRUCT['label_vals'].items():
            if (k == 'created') or (k == 'updated'):
                self.dfob[k] = self.dfob['Позначка часу'].dt.strftime(v)
            else:
                self.dfob[k] = str(v)

        # Створимо список полів фронтматерії
        fm_fields = list(self.TBL_STRUCT['label_refs'].keys()) + \
                    list(self.TBL_STRUCT['label_vals'].keys())
        fm_fields.remove('title')
        fm_fields.remove('tags')
        fm_fields = ['tags',] + fm_fields
        self.FRONTMATTER_FIELDS = fm_fields

    def create_notes(self):
        ''' Створення нотаток у сховищі Обсідіан з вх. таблиці Гугл Форм '''
        def create_note(row):
            ''' Створення і збереження однієї нотатки з одного рядка таблиці '''
            frontmatter = "---\n"
            for field in self.FRONTMATTER_FIELDS:
                frontmatter += f"{field.lower()}: {row[field]}\n"
            frontmatter += '---\n\n'

            content = ""
            for col in self.TBL_STRUCT['sections']:
                content += f"## {col}\n\n{row[col]}\n\n"

            path = os.path.join(self.vault_dir, notes_subdir, row.title + '.md')

            with open(path, "w", encoding="utf-8") as f:
                f.write(frontmatter + content)

        # Визначити субфолдер розташування нотаток
        notes_subdir = self.TBL_STRUCT['subdir'] if self.is_clean_writing else 'TMP'
            
        # Залишаємо у таблиці dfob лише нові назви, тобто такі, що відсутні у сховищі
        n_dfob_notes = len(self.dfob)
        if self.not_write_dupl:
            idx_new_notes = ~(self.dfob.title + '.md').isin(self.all_notes)
            n_new_notes = idx_new_notes.sum()
            self.dfob = self.dfob.loc[idx_new_notes]
            print(f'❗ З {n_dfob_notes} записів в таблиці всього нових {n_new_notes}')
        # Створення і збереження однієї нотатки з одного рядка таблиці
        for _, row in self.dfob.iterrows():
            create_note(row)

        print(f'✅ У субфолдері {self.vault + notes_subdir} створено '
              f'{len(self.dfob)} нотаток: {list(self.dfob.title)}')

    def main(self, table: str):
        ''' Основоний метод класу `GS2ON_Convertor` '''
        # Зчитуємо вхідні дані з таблиці Гугл Форми і опис її конвертування до Обсідіан
        self.read_gs_table(table)

        # Валідація структури вх. таблиці Гугл Форми і словника з описом конвертування 
        # цієї таблиці до Обсідіан
        self.check_table_struct()

        # Перетворення значень стовпчиків зі списку `TBL_STRUCT['pers_name']` з 
        # вхідного датафрейму: "Прізвище Ім'я По-батькові" -> "Ім'я Прізвище"
        self.pib2ip()

        # Перетворення значень стовпчиків зі списку `TBL_STRUCT['linked']` з 
        # вхідного датафрейму у внутрішнє Обсідіан-посилання: name -> [[name]]
        self.make_linked()

        # Копія таблиці зі скороченими назвами стовпчиків
        self.dfgf2dfob()

        # Перевірка відсутності дублікатів імен нотаток у вх. таблиці
        self.check_dupl_in_table()

        # Завершення підготовки Обсідіан таблиці перед конвертацією у нотатки
        self.complete_obs_table()

        # Створення нотаток у сховищі Обсідіан з вх. таблиці Гугл Форм
        self.create_notes()

if __name__ == '__main__':
    folders = {
        'drive_base': 'D:/boa_uniteam/',
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
