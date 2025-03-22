REM створення списку пакетів віртуального середовища `gis`:
conda list --name gis --export > package-list.txt

REM Створення віртуального середовища зі списку пакетів `package-list.txt`:
REM conda create -n myenv –file package-list.txt