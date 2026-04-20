# Seed SubjectTemplates and CurriculumSubjects for School/Madrasah (Science, Arts, Commerce)

from django.db import migrations


def seed_templates(apps, schema_editor):
    SubjectTemplate = apps.get_model('curriculum', 'SubjectTemplate')
    # (code, name, theory, practical, is_elective, display_order)
    templates = [
        ('BANGLA', 'Bangla', 100, 0, False, 1),
        ('ENGLISH', 'English', 100, 0, False, 2),
        ('MATH', 'Mathematics', 100, 0, False, 3),
        ('SCIENCE', 'General Science', 100, 0, False, 4),
        ('SOCIAL_SCI', 'Social Science', 100, 0, False, 5),
        ('RELIGION', 'Religion / Islamic Studies', 100, 0, False, 6),
        ('BGS', 'Bangladesh and Global Studies', 100, 0, False, 7),
        ('ICT', 'Information and Communication Technology', 50, 50, False, 8),
        # Madrasah
        ('QURAN', 'Quran Majeed', 100, 0, False, 10),
        ('HADITH', 'Hadith', 100, 0, False, 11),
        ('ARABIC', 'Arabic', 100, 0, False, 12),
        ('AQAID_FIQH', 'Aqaid and Fiqh', 100, 0, False, 13),
        ('MADRASAH_SCI', 'Science (Madrasah)', 100, 0, False, 14),
        ('MADRASAH_MATH', 'Mathematics (Madrasah)', 100, 0, False, 15),
        # HSC Science
        ('PHYSICS', 'Physics', 100, 50, False, 20),
        ('CHEMISTRY', 'Chemistry', 100, 50, False, 21),
        ('BIOLOGY', 'Biology', 100, 50, False, 22),
        ('HIGHER_MATH', 'Higher Mathematics', 100, 0, False, 23),
        ('ENGLISH_HSC', 'English (HSC)', 100, 0, False, 24),
        # HSC Arts
        ('CIVICS', 'Civics', 100, 0, False, 30),
        ('ECONOMICS', 'Economics', 100, 0, False, 31),
        ('HISTORY', 'History', 100, 0, False, 32),
        ('LOGIC', 'Logic', 100, 0, False, 33),
        ('GEOGRAPHY', 'Geography', 100, 0, False, 34),
        ('ISLAMIC_HIST', 'History of Islam', 100, 0, False, 35),
        # HSC Commerce
        ('ACCOUNTING', 'Accounting', 100, 0, False, 40),
        ('BUSINESS_ORG', 'Business Organization and Management', 100, 0, False, 41),
        ('PRODUCTION', 'Production Management and Marketing', 100, 0, False, 42),
        ('FINANCE', 'Finance and Banking', 100, 0, False, 43),
        # Electives
        ('AGRICULTURE', 'Agricultural Studies', 100, 0, True, 50),
        ('HOMESCI', 'Home Science', 100, 0, True, 51),
    ]
    for code, name, theory, practical, elective, order in templates:
        SubjectTemplate.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'default_theory_marks': theory,
                'default_practical_marks': practical,
                'is_elective': elective,
                'display_order': order,
            },
        )


def seed_curriculum_subjects(apps, schema_editor):
    Curriculum = apps.get_model('curriculum', 'Curriculum')
    CurriculumLevel = apps.get_model('curriculum', 'CurriculumLevel')
    Stream = apps.get_model('curriculum', 'Stream')
    SubjectTemplate = apps.get_model('curriculum', 'SubjectTemplate')
    CurriculumSubject = apps.get_model('curriculum', 'CurriculumSubject')

    def get_template(code):
        return SubjectTemplate.objects.get(code=code)

    def get_cls(curriculum_code, level_num, stream_code=None):
        c = Curriculum.objects.get(code=curriculum_code)
        lvl = CurriculumLevel.objects.get(curriculum=c, level_number=level_num)
        stream = Stream.objects.filter(code=stream_code).first() if stream_code else None
        return (c, lvl, stream)

    def link(curriculum, level, stream, template_code, compulsory=True, order=0):
        t = get_template(template_code)
        CurriculumSubject.objects.get_or_create(
            curriculum=curriculum,
            level=level,
            stream=stream,
            subject_template=t,
            defaults={'is_compulsory': compulsory, 'display_order': order},
        )

    # Ebtedayi 1-5: common subjects
    for level_num in range(1, 6):
        c, lvl, stream = get_cls('Ebtedayi', level_num, None)
        for i, code in enumerate(['BANGLA', 'ENGLISH', 'MATH', 'SCIENCE', 'QURAN', 'HADITH', 'ARABIC', 'AQAID_FIQH', 'SOCIAL_SCI'], 1):
            link(c, lvl, stream, code, True, i)

    # Dakhil 6-10: common subjects
    for level_num in range(6, 11):
        c, lvl, stream = get_cls('Dakhil', level_num, None)
        for i, code in enumerate([
            'BANGLA', 'ENGLISH', 'MATH', 'MADRASAH_SCI', 'QURAN', 'HADITH', 'ARABIC',
            'AQAID_FIQH', 'BGS', 'ICT', 'SOCIAL_SCI',
        ], 1):
            link(c, lvl, stream, code, True, i)

    # SSC 1-10: common
    for level_num in range(1, 11):
        c, lvl, stream = get_cls('SSC', level_num, None)
        for i, code in enumerate(['BANGLA', 'ENGLISH', 'MATH', 'SCIENCE', 'SOCIAL_SCI', 'RELIGION', 'BGS', 'ICT'], 1):
            link(c, lvl, stream, code, True, i)

    # HSC Science 11-12: common + stream
    for level_num in [11, 12]:
        c, lvl, stream = get_cls('HSC-Science', level_num, None)
        for i, code in enumerate(['BANGLA', 'ENGLISH_HSC', 'ICT'], 1):
            link(c, lvl, stream, code, True, i)
        c, lvl, stream = get_cls('HSC-Science', level_num, 'Science')
        for i, code in enumerate(['PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'HIGHER_MATH'], 1):
            link(c, lvl, stream, code, True, i)

    # HSC Arts 11-12
    for level_num in [11, 12]:
        c, lvl, stream = get_cls('HSC-Arts', level_num, None)
        for i, code in enumerate(['BANGLA', 'ENGLISH_HSC', 'ICT'], 1):
            link(c, lvl, stream, code, True, i)
        c, lvl, stream = get_cls('HSC-Arts', level_num, 'Arts')
        for i, code in enumerate(['CIVICS', 'ECONOMICS', 'HISTORY', 'GEOGRAPHY', 'LOGIC', 'ISLAMIC_HIST'], 1):
            link(c, lvl, stream, code, True, i)

    # HSC Commerce 11-12
    for level_num in [11, 12]:
        c, lvl, stream = get_cls('HSC-Commerce', level_num, None)
        for i, code in enumerate(['BANGLA', 'ENGLISH_HSC', 'ICT'], 1):
            link(c, lvl, stream, code, True, i)
        c, lvl, stream = get_cls('HSC-Commerce', level_num, 'Commerce')
        for i, code in enumerate(['ACCOUNTING', 'BUSINESS_ORG', 'PRODUCTION', 'FINANCE'], 1):
            link(c, lvl, stream, code, True, i)


def reverse_seed_templates(apps, schema_editor):
    SubjectTemplate = apps.get_model('curriculum', 'SubjectTemplate')
    codes = [
        'BANGLA', 'ENGLISH', 'MATH', 'SCIENCE', 'SOCIAL_SCI', 'RELIGION', 'BGS', 'ICT',
        'QURAN', 'HADITH', 'ARABIC', 'AQAID_FIQH', 'MADRASAH_SCI', 'MADRASAH_MATH',
        'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'HIGHER_MATH', 'ENGLISH_HSC',
        'CIVICS', 'ECONOMICS', 'HISTORY', 'LOGIC', 'GEOGRAPHY', 'ISLAMIC_HIST',
        'ACCOUNTING', 'BUSINESS_ORG', 'PRODUCTION', 'FINANCE', 'AGRICULTURE', 'HOMESCI',
    ]
    SubjectTemplate.objects.filter(code__in=codes).delete()


def reverse_seed_curriculum_subjects(apps, schema_editor):
    CurriculumSubject = apps.get_model('curriculum', 'CurriculumSubject')
    CurriculumSubject.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_seed_bd_streams_and_curricula'),
    ]

    operations = [
        migrations.RunPython(seed_templates, reverse_seed_templates),
        migrations.RunPython(seed_curriculum_subjects, reverse_seed_curriculum_subjects),
    ]
