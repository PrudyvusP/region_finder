# region_finder

![region_finder_workflow](https://github.com/PrudyvusP/region_finder/actions/workflows/main.yml/badge.svg)

### Пролог
Region_finder - это мини-проект для осуществления поиска региона РФ в 
адресной строке.

В будущем планируется, что Region_finder станет отдельным микросервисом, так 
как функционал проекта используется в нескольких веб-сервисах.

Особенностью этого проекта в сравнении с другими проектами автора является 
уход от фласковых оберток для SQLAlchemy и Alembic.

### Установка & использование 

Осуществим подготовку необходимой среды:  
```bash
python3 -m venv venv && source venv/bin/activate && pip3 install region_finder_ru-0.0.2-py3-none-any.whl && pip3 install -r requirements.txt && cd alembic && alembic upgrade head && cd .. 
```

Загрузим необходимые данные и заполним эталонными сведениями таблицы:
```bash
wget -O P_Indx.zip https://www.pochta.ru/assets/P_Indx17_dd0031ca43.zip && unzip P_Indx.zip -d data && rm P_Indx.zip && python3 persisting.py data/PIndx17.dbf
```

Определим регионы во всех адресных строках из файла:
```bash
python3 main.py input.txt
```

Результат работы программы отразится в stdout

### Ограничения
- Города с одинаковыми названиями, расположенные в разных регионах 
  игнорируются (г. Советск или г. Железногорск).
- Библиотека [region_finder_ru](https://github.com/PrudyvusP/region_finder_ru) устанавливается вручную, так как отсутствует 
  в pypi.org в данный момент.
- В качестве БД используется SQLite для упрощения демонстрации. В реальном 
  проекте безусловно кредиты СУБД прячутся и настраиваются, например, через 
  переменные окружения.