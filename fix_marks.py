import os
import random
import argparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django

django.setup()
from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()


def create_commendation(schoolkid, subject_name):
    commendation_text = ['Молодец!',
                         'Отлично!',
                         'Хорошо!',
                         'Великолепно!',
                         'Ты на верном пути!'
                         ]
    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                   group_letter=schoolkid.group_letter,
                                   subject__title=subject_name).order_by('?').first()
    Commendation.objects.create(text=random.choice(commendation_text),
                                created=lesson.date,
                                schoolkid=schoolkid,
                                subject=lesson.subject,
                                teacher=lesson.teacher)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Программа улучшает успеваемость в онлайн дневнике')
    parser.add_argument(
        '-kidn', '--schoolkid_name', help='Имя ученика', type=str, default='Иван')
    parser.add_argument(
        '-kids', '--schoolkid_surname', help='Фамилия ученика', type=str, default='Фролов')
    parser.add_argument(
        '-subj', '--subject_name', help='Название предмета', type=str, default='Музыка')
    args = parser.parse_args()
    schoolkid_name = f'{args.schoolkid_surname} {args.schoolkid_name}'
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f'Ученик не найден, уточните имя {schoolkid_name}')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников, уточните имя')
    else:
        print(f'Ученик найден...{schoolkid_name}')
        fix_marks(schoolkid)
        print('исправляем оценки')
        remove_chastisements(schoolkid)
        print('удаляем замечания')
        try:
            create_commendation(schoolkid, args.subject_name)
            print(f'добавляем похвалу по предмету...{args.subject_name}')
        except IndexError:
            print(f'Предмет {args.subject_name} не найдет, проверьте название')
