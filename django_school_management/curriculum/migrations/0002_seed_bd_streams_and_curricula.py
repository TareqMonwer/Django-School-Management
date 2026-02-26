# Data migration: seed BD streams and curricula (Ebtedayi, Dakhil, SSC, HSC)

from django.db import migrations


def get_madrasah_board(apps):
    EducationBoard = apps.get_model('institute', 'EducationBoard')
    return EducationBoard.objects.filter(country='BD', name__icontains='Madrasah').first()


def seed_streams(apps, schema_editor):
    Stream = apps.get_model('curriculum', 'Stream')
    streams = [
        {'name': 'Science', 'code': 'Science', 'display_order': 1},
        {'name': 'Arts', 'code': 'Arts', 'display_order': 2},
        {'name': 'Commerce', 'code': 'Commerce', 'display_order': 3},
    ]
    for s in streams:
        Stream.objects.get_or_create(code=s['code'], defaults=s)


def seed_curricula_and_levels(apps, schema_editor):
    Curriculum = apps.get_model('curriculum', 'Curriculum')
    CurriculumLevel = apps.get_model('curriculum', 'CurriculumLevel')
    board = get_madrasah_board(apps)

    # Madrasah Ebtedayi: class 1–5
    ebtedayi, _ = Curriculum.objects.get_or_create(
        code='Ebtedayi',
        defaults={
            'name': 'Madrasah Ebtedayi',
            'description': 'Ebtedayi (primary) level, Class 1–5, under Bangladesh Madrasah Education Board.',
            'board_id': board.pk if board else None,
            'institute_type': 'madrasah',
            'is_active': True,
            'display_order': 10,
        },
    )
    for n in range(1, 6):
        CurriculumLevel.objects.get_or_create(
            curriculum=ebtedayi,
            level_number=n,
            defaults={
                'name': f'Class {n}',
                'semester_number': n,
                'streams_applicable': False,
                'display_order': n,
            },
        )

    # Madrasah Dakhil: class 6–10
    dakhil, _ = Curriculum.objects.get_or_create(
        code='Dakhil',
        defaults={
            'name': 'Madrasah Dakhil',
            'description': 'Dakhil (secondary) level, Class 6–10, under Bangladesh Madrasah Education Board.',
            'board_id': board.pk if board else None,
            'institute_type': 'madrasah',
            'is_active': True,
            'display_order': 20,
        },
    )
    for n in range(6, 11):
        CurriculumLevel.objects.get_or_create(
            curriculum=dakhil,
            level_number=n,
            defaults={
                'name': f'Class {n}',
                'semester_number': n,
                'streams_applicable': False,
                'display_order': n,
            },
        )

    # SSC (school): class 1–10
    ssc, _ = Curriculum.objects.get_or_create(
        code='SSC',
        defaults={
            'name': 'SSC (School)',
            'description': 'School curriculum up to SSC, Class 1–10.',
            'board_id': None,
            'institute_type': 'school',
            'is_active': True,
            'display_order': 30,
        },
    )
    for n in range(1, 11):
        CurriculumLevel.objects.get_or_create(
            curriculum=ssc,
            level_number=n,
            defaults={
                'name': f'Class {n}',
                'semester_number': n,
                'streams_applicable': False,
                'display_order': n,
            },
        )

    # HSC Science / Arts / Commerce (school): class 11–12 with streams
    for label, code_suffix in [('Science', 'HSC-Science'), ('Arts', 'HSC-Arts'), ('Commerce', 'HSC-Commerce')]:
        hsc, _ = Curriculum.objects.get_or_create(
            code=code_suffix,
            defaults={
                'name': f'HSC {label}',
                'description': f'HSC (Higher Secondary) {label} group, Class 11–12.',
                'board_id': None,
                'institute_type': 'school',
                'is_active': True,
                'display_order': 40 if label == 'Science' else 41 if label == 'Arts' else 42,
            },
        )
        for n in [11, 12]:
            CurriculumLevel.objects.get_or_create(
                curriculum=hsc,
                level_number=n,
                defaults={
                    'name': f'Class {n}',
                    'semester_number': n,
                    'streams_applicable': True,
                    'display_order': n,
                },
            )


def reverse_seed_streams(apps, schema_editor):
    Stream = apps.get_model('curriculum', 'Stream')
    Stream.objects.filter(code__in=['Science', 'Arts', 'Commerce']).delete()


def reverse_seed_curricula(apps, schema_editor):
    Curriculum = apps.get_model('curriculum', 'Curriculum')
    CurriculumLevel = apps.get_model('curriculum', 'CurriculumLevel')
    CurriculumLevel.objects.filter(
        curriculum__code__in=['Ebtedayi', 'Dakhil', 'SSC', 'HSC-Science', 'HSC-Arts', 'HSC-Commerce']
    ).delete()
    Curriculum.objects.filter(
        code__in=['Ebtedayi', 'Dakhil', 'SSC', 'HSC-Science', 'HSC-Arts', 'HSC-Commerce']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0001_initial_curriculum_library'),
        ('institute', '0015_educationboard'),
    ]

    operations = [
        migrations.RunPython(seed_streams, reverse_seed_streams),
        migrations.RunPython(seed_curricula_and_levels, reverse_seed_curricula),
    ]
