import yaml
import pandas as pd
import sys
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

    def __init__(self, folders: dict):
        ''' Встановлюємо повні шляхи до фолдерів коду і даних '''
        # Кореневі дректорії компа
        base = folders['base']
        
        # Конфігурація робочих директорій
        self.code_dir = base + folders['vaults_storage'] + folders['code_dir']
        self.data_dir = base + folders['vaults_storage'] + folders['data_dir']
        
        # надання доступу до фолдера коду
        sys.path.insert(0, self.code_dir)
        
        # Константи алгоритму
        self.config_file = self.code_dir + 'config.yml'
        self.config_gs_file = self.code_dir + 'config_gs.yml'
        self.cred_file = self.code_dir + 'credentials.json'
        
        # Створення конфігураційного словника self.conf
        self.read_yaml_config()

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
            sys.exit(f'🚩 Таблиця `{table}` відсутня серед таблиць {tables}')

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
            sys.exit(f'🚩 Таблиця `{table}` порожня!')
        else:
            print(f'✅ Розмір таблиці `{table}` - {self.dfgf.shape}')

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
            sys.exit(f'🚩 Структурні проблеми в таблиці `{self.table}` такі: {problems}')
        else:
            print(f'✅ Валідація відповідності структури таблиці `{self.table}` пройдена')

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
            linked_names = ['[[' + s + ']]' for _, s in self.dfgf[name].items()]
            self.dfgf[name] = linked_names

    def dfgf2dfob(self):
        ''' Копія таблиці зі скороченими назвами стовпчиків - назви міток 
        фронтматерії. Таблиця готується для формування нотаток Обсідіан.
        '''
        # Пряма і зворотня мапи (мітки нотаток Обсідіан) <--> (назви стовпчиків таблиці Гугл Форми)
        dfob_cols = self.TBL_STRUCT['label_refs']
        dfob_cols_i = {v: k for k, v in dfob_cols.items()}
    
        dfob = self.dfgf.copy()
        dfob.rename(columns=dfob_cols_i, inplace=True)
        if 'title' not in dfob.columns:
            dfob['title'] = self.dfgf[dfob_cols['title']]

        self.dfob_cols = dfob_cols
        self.dfob = dfob

    def check_duplicates(self):
        ''' Перевірка відсутності дублікатів імен нотаток '''
        idx_dfob_dupl = self.dfob.duplicated(subset='title', keep=False)
        dfgf_dupl = self.dfgf.loc[idx_dfob_dupl]
        if len(dfgf_dupl) > 0:
            print(f'🚩 У таблиці {self.table} виявлені дублікати назв нотаток:')
            print(self.dfgf[self.dfob_cols['title']].to_markdown())
            sys.exit('⚠️ Усуньте дублікати і повторіть спробу.')
        return

