"""
Curriculum library: reusable definitions of curricula, levels, streams, and subjects.

Supports:
- Madrasah Board (BD): Ebtedayi (class 1–5), Dakhil (6–10/12) with different subjects per class.
- School boards (BD): SSC/HSC with Science, Commerce, Arts groups and common vs stream-specific subjects.
- Elective subjects across institutes.
- Institute-level customizability via optional curriculum assignment and overrides.

Design:
- Curriculum = a named track (e.g. "Madrasah Ebtedayi", "Madrasah Dakhil", "HSC Science").
- CurriculumLevel = class/level within a curriculum (e.g. Class 1, Class 9).
- Stream = group (Science, Arts, Commerce) used when a level has stream-specific subjects.
- SubjectTemplate = reusable subject definition (name, code, marks); no instructor (runtime).
- CurriculumSubject = which subject (template) is offered at which level, optional stream, compulsory/elective.
"""

from model_utils.models import TimeStampedModel
from django_prometheus.models import ExportModelOperationsMixin

from django.db import models


class Curriculum(ExportModelOperationsMixin('curriculum'), TimeStampedModel):
    """
    A named curriculum track (e.g. Madrasah Ebtedayi, Dakhil, SSC, HSC Science).
    Optional link to board and institute type for filtering.
    """
    name = models.CharField(max_length=120)
    code = models.CharField(
        max_length=40,
        blank=True,
        help_text='Short code for display (e.g. Ebtedayi, Dakhil, HSC-Science).',
    )
    description = models.TextField(blank=True)
    # Filtering: which board / institute type this curriculum applies to
    board = models.ForeignKey(
        'institute.EducationBoard',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='curricula',
        help_text='Education board (e.g. Bangladesh Madrasah Board). Optional.',
    )
    institute_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('', 'Any'),
            ('school', 'School (SSC/HSC)'),
            ('madrasah', 'Madrasah (Ebtedayi/Dakhil/Alim)'),
            ('polytechnic', 'Polytechnic'),
        ],
        help_text='Institute type this curriculum is intended for. Blank = any.',
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0, help_text='Order in lists.')

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Curricula'

    def __str__(self):
        return self.name or self.code or str(self.pk)


class CurriculumLevel(ExportModelOperationsMixin('curriculum_level'), TimeStampedModel):
    """
    A class/level within a curriculum (e.g. Class 1, Class 9, Ebtedayi 5).
    semester_number maps to the academy's Semester.number (1–12) when used.
    """
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        related_name='levels',
    )
    level_number = models.PositiveSmallIntegerField(
        help_text='Numeric level (1–12). Used to map to Semester/Class number.',
    )
    name = models.CharField(
        max_length=80,
        help_text='Display name (e.g. "Class 1", "Ebtedayi 5", "Dakhil 9").',
    )
    # When an institute uses Semester model, this maps level to semester number (1–12)
    semester_number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Maps to Semester.number (1–12) when curriculum is applied. Defaults to level_number.',
    )
    # True when this level has stream-specific subjects (e.g. HSC Class 11/12 Science vs Arts)
    streams_applicable = models.BooleanField(
        default=False,
        help_text='If True, subjects may be defined per stream (Science/Arts/Commerce) for this level.',
    )
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['curriculum', 'display_order', 'level_number']
        unique_together = [('curriculum', 'level_number')]

    def __str__(self):
        return f'{self.curriculum}: {self.name}'

    @property
    def effective_semester_number(self):
        return self.semester_number if self.semester_number is not None else self.level_number


class Stream(ExportModelOperationsMixin('stream'), TimeStampedModel):
    """
    Stream/group (Science, Arts, Commerce). Shared across curricula where levels use streams.
    """
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=20, unique=True, help_text='e.g. Science, Arts, Commerce.')
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class SubjectTemplate(ExportModelOperationsMixin('subject_template'), TimeStampedModel):
    """
    Reusable subject definition in the curriculum library.
    No instructor or institute — those are set when creating runtime Subject instances.
    """
    name = models.CharField(max_length=120)
    code = models.CharField(
        max_length=30,
        unique=True,
        help_text='Unique code (e.g. 101, BANGLA, MATH).',
    )
    description = models.TextField(blank=True)
    default_theory_marks = models.PositiveIntegerField(default=100)
    default_practical_marks = models.PositiveIntegerField(default=0)
    is_elective = models.BooleanField(
        default=False,
        help_text='If True, typically offered as an optional/elective subject.',
    )
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return f'{self.name} ({self.code})'


class CurriculumSubject(ExportModelOperationsMixin('curriculum_subject'), TimeStampedModel):
    """
    Links a subject (template) to a curriculum level, optionally to a stream.
    - stream=None: subject is common to all streams at this level.
    - stream=Science: subject is for Science stream only at this level.
    """
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        related_name='curriculum_subjects',
    )
    level = models.ForeignKey(
        CurriculumLevel,
        on_delete=models.CASCADE,
        related_name='subjects',
    )
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='curriculum_subjects',
        help_text='Null = common to all streams; set for stream-specific subjects.',
    )
    subject_template = models.ForeignKey(
        SubjectTemplate,
        on_delete=models.CASCADE,
        related_name='curriculum_subject_entries',
    )
    is_compulsory = models.BooleanField(
        default=True,
        help_text='If False, subject is elective at this level/stream.',
    )
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['curriculum', 'level', 'stream', 'display_order', 'subject_template']
        unique_together = [('curriculum', 'level', 'stream', 'subject_template')]
        verbose_name = 'Curriculum subject'
        verbose_name_plural = 'Curriculum subjects'

    def __str__(self):
        stream_part = f' [{self.stream}]' if self.stream else ''
        return f'{self.curriculum} / {self.level}{stream_part}: {self.subject_template}'
