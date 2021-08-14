import os
import random
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


def create_commendation(schoolkid, subject):
    commendation_text = ['Молодец!',
                         'Отлично!',
                         'Хорошо!',
                         'Великолепно!',
                         'Ты на верном пути!'
                         ]
    lesson = random.choice(Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                                 group_letter=schoolkid.group_letter,
                                                 subject__title=subject))
    Commendation.objects.create(text=random.choice(commendation_text),
                                created=lesson.date,
                                schoolkid=schoolkid,
                                subject=lesson.subject,
                                teacher=lesson.teacher)


# schoolkid_name = 'Фролов Иван'
# schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name)[0]
# fix_marks(schoolkid)
# remove_chastisements(schoolkid)
# math_6A = Lesson.objects.filter(year_of_study=6, group_letter='А', subject__title='Математика')

if __name__ == '__main__':
    schoolkid_name = 'Фролов Иван'
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    fix_marks(schoolkid)
    remove_chastisements(schoolkid)
    create_commendation(schoolkid, 'Музыка')
