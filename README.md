# Исправление успеваемости ученика в электронном дневнике

Программа исправляет оценки `2` и `3` на `5`. Удаляет замечания. Добавляет похвалы за работу на уроке.
Исходный код проекта и базу данных можно получить по ссылке: [dvmn.org GitHub](https://github.com/devmanorg/e-diary "dvmn.org GitHub")
Архив исходной базы данных - [Архив базы данных](https://dvmn.org/filer/canonical/1562234129/166/  "Архив базы данных") 

## Как использовать

### Установка

- Скачайте и установите исходный код проекта по ссылке - [dvmn.org GitHub](https://github.com/devmanorg/e-diary "dvmn.org GitHub") 
- Запустите сервер `python manage.py runserver`
- Скачайте код `fix_marks.py` в папку с проектом
- Для работы скачайте Python - https://www.python.org/
- Запустите программу `python fix_marks.py`
- Обновите страницу. Проверьте, что изменения внесены.
Для `Фролов Иван` будет удалены все замечания и исправлены оценки `2` и `3` на `5`. Будет добавлена похвала по предмету `Музыка`.

### Исправить оценки другому ученику

- Запустите программу с ключами `python fix_marks.py -kidn Петр -kids Петров -subj Математика`
Для `Петр Петров` будет удалены все замечания и исправлены оценки `2` и `3` на `5`. Будет добавлена похвала по предмету `Математика`.

#### Аргументы

- `-kidn`, `--schoolkid_name`, Имя ученика, строка, по умолчанию `Иван`
- `-kids`, `--schoolkid_surname`, Фамилия ученика, строка, по умолчанию `Фролов`
- `-subj`, `--subject_name`, Название предмета, строка, по умолчанию `Музыка`

#### Ошибки

-Ученик не найден, уточните имя {Имя Фамилия}
Ученик с {Имя Фамилия} не найден уточните правильность написания и проверьте, что такой ученик существует.

-Найдено несколько учеников, уточните имя {Имя Фамилия}
Найдено несколько учеников, уточните поиск.

-Предмет {Название предмета} не найдет, проверьте название
Предмет с таким названием не найдет, уточните название на наличие ошибок написания.

-'Уроки не найдены, уточните предмет'
Уроки для класса ученика не найдены. Проверьте есть ли уроки по предмету у ученика.

## Подробнее о работе программы

Программа `fix_marks.py` вносит изменения в локальную базу данных 'schoolbase.sqlite3'

### Описание моделей

На сайте есть ученики: `Schoolkid`. Класс ученика определяется через комбинацию его полей `year_of_study` — год обучения и `group_letter` — литера класса. Вместе получается, например, 10А. Ученик связан со следующими моделями:

- `Mark` — оценка на уроке, от 2 до 5.
- `Commendation` — похвала от учителя, за особые достижения.
- `Chastisement` — замечание от учителя, за особые проступки.

Все 3 объекта связаны не только с учителем, который их создал, но и с учебным предметом (`Subject`). Примеры `Subject`:

- Математика 8 класса
- Геометрия 11 класса
- Русский язык 1 класса
- Русский язык 4 класса

`Subject` определяется не только названием, но и годом обучения, для которого учебный предмет проходит.

За расписание уроков отвечает модель `Lesson`. Каждый объект `Lesson` — урок в расписании. У урока есть комбинация `year_of_study` и `group_letter`, благодаря ей можно узнать для какого класса проходит этот урок. У урока есть `subject` и `teacher`, которые отвечают на вопросы "что за урок" и "кто ведёт". У урока есть `room` — номер кабинета, где он проходит. Урок проходит в дату `date`.

Расписание в школе строится по слотам:

- 8:00-8:40 — 1 урок
- 8:50-9:30 — 2 урок
- ...

У каждого `Lesson` есть поле `timeslot`, которое объясняет, какой номер у этого урока в расписании.


## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).