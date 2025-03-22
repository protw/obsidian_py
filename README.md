### Перенесення даних форм з Гугл таблиць у нотатки Обсідіан

250302

### Короткий опис ідеї

#### Мета проєкту

Створення робочого простору Національного Контактного Пункту (НКП) New European Bauhaus (NEB) на базі Університету Григорія Сковороди у Переяславі (УГСП) з використанням інструменту Obsiidan з допомогою команди Національного Екологічного Центру України (НЕЦУ)

#### Проблеми, які вирішує проект

- Системний підхід в допомозі українським учасникам щодо формування проєктних заявок  на євпропейських грантові проєкти
- Систематизація європейських та українських партнерів і консорціумів, програм і конкурсів, зокрема, в програмі НЄБ Горизонт Європа, але не обмежуючись останньою
- Утворення і підтримка мережевої взаємодії заявників

#### Очікувані результати та вплив

- Зростання кількості поданих заявок укр заявниками
- Зростання кількості отриманих грантів укр заявниками
- Кращі показники роботи (KPI) НКП-НЄБ

#### Плановані етапи роботи

1. Створення робочого простору Національного Контактного Пункту (НКП) New European Bauhaus (NEB) на базі Університету Григорія Сковороди у Переяславі ([[УГСП]]) з використанням інструменту Obsidan з допомогою команди Національного Екологічного Центру України ([[НЕЦУ]])
2. Наповнення робочого простору НКП-НЄБ з одночасним навчанням членів команди у користуванні ним (*LBD - learning-by-doing*).
3. Використання робочого простору НКП-НЄБ у якості: довідника, засобу планування, аналізу і моніторингу виконання.

### Члени команди

- [[УГСП]]: [[Олеся Скляренко]]
- [[НЕЦУ]]: [[Євген Бовсуновський]], [[Віталій Гулевець]], [[Юлія Христинченко]]

### Наявні і бажані партнери

**Наявні**:
- УГСП

**Бажані**:

- Ігор Таранов, Начальник відділу, Офіс Горизонт Європа в Україні, https://horizon-europe.org.ua/
- Тетяна Федонюк,  НКП "*Кластер 6: продовольство, біоекономіка, природні ресурси, сільське господарство та навколишнє середовище*", Поліський Національний університет
- Анжела Пятова, НКП “*Клімат, енергетика та мобільність*”, КПІ

### Структура даних РП НКП-НЄБ

**Основні змістовні дані**:
1. `PERSONS`: Персоналії
2. `ORGS`: Організації (партнери, спонсори)
3. `TEAMS`: Команди (заявники, підрозділи, НКП)
4. `CALLS`: Тематичні конкурси (calls), оголошення
5. `DOCS`: Програмні документи, 
6. `PROJ`: Проєкти (проєктні заявки зі статусом - ідея, заявка готується, заявка подана, заявка припинена, заявці відмовлено, заявка прийнята, проєкт виконується, проєкт успішно завершений)


**Інші функціональні фолдери**: 
1. `COMMON`: фолдери загального використання - медіа файли, шаблони, інше 
2. `CURRENT`: поточні нотатки щодо загальних питань
3. `QUERIES`: аналітичні запити
4. `REGLAMENT`: опис структур, процедури і правила користування вікі-сховищем
	- `REGLAMENT/FORMS`: Форми, які можуть заповнювати зовнішні користувачі:
		1. Г-форма для персоналій
		2. Г-форма для організацій
		3. Г-форма для команд
		4. Г-форма для проєктних ідей
		5. процедура перенесення даних форм у Обсідіан

### Перенесення даних форм з Гугл таблиць у нотатки Обсідіан

Тут наведений загальний опис алгоритму. Докладніше ідеї щодо окремих фрагментів алгоритму представлені тут [250303\_Перенесення\_Гугл\_таблиць\_у\_нотатки\_Обсідіан.md](250303_Перенесення_Гугл_таблиць_у_нотатки_Обсідіан.md).

**Основні блоки коду**:

1. Для кожної Г-форми визначити такі фолдери і файли: (1) де розміщена таблиця відповідей Г-форми, (2) де збирати всі назви нотаток, (3) куди складати нові нотатки, (4) куди складати лог виконаної процедури.
2. Для кожної Г-форми визначити словник, що пов'язує довгі назви стовпчиків таблиці відповідей Г-форми (укр, з пунктуаціями) з короткими назвами полів у датафреймі (лат, маленькими, без пунктуацій).
3. Зчитування таблиці відповідей Г-форми і заміна довгих назв стовпчиків на короткі. Згенерувати назви нотаток для кожного рядка (запису) таблиці. Нормалізувати назви нотаток (не більше 1 пробілу між словами всередині і без пробілів по краях). Виявити дублікати власне в таблиці і, у разі наявності, **зупинити виконання** та запропонувати оператору розібратися з ними, надавши список імен дублікатів.
4. Зчитати всі назви нотаток (імена файлів без шляху і без розширення) з фолдеру (п. 1.2 вище). Знайти ненормалізовані назви нотаток (більше 1 пробілу між словами всередині і є пробіли по краях). **Зупинити виконання** та запропонувати оператору розібратися з ненормалізованими назвами нотаток, надавши список їхніх імен і шляхів. Виявити дублікати назв нотаток у Обсідіан сховищі і, у разі наявності, **зупинити виконання** та запропонувати оператору розібратися з ними, надавши список імен і шляхів дублікатів.
5. На кожну зупинку у пп. 3 і 4 записати окремий лог у фолдері п. 1.4.
6. Після безпомилкового проходження пп. 3 і 4, порівняти назви нотаток з цих двох списків і скласти список нових назв зі списку п. 3. Для кожної нової назви нотатки із цього переліку створити повний текст нотатки і зберегти її під цим новим іменем у фолдері п. 1.3. За результатом виконання записати окремий лог у фолдері п. 1.4.