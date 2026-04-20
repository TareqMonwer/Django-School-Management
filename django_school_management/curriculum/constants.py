"""
Curriculum library constants for Bangladesh (BD).

Madrasah Board (Bangladesh Madrasah Education Board):
- Ebtedayi: primary level, class 1–5
- Dakhil: secondary, class 6–10 (or 6–12 in some setups)

School boards (e.g. Dhaka, Rajshahi):
- SSC: class 1–10, then SSC exam
- HSC: class 11–12 with streams (Science, Arts, Commerce)

Streams (used for HSC and optionally Dakhil/SSC):
- Science, Arts, Commerce (align with institute/education_boards.BD_GROUPS)
"""

from django_school_management.institute.education_boards import (
    BD_GROUP_SCIENCE,
    BD_GROUP_ARTS,
    BD_GROUP_COMMERCE,
)

# Curriculum codes (match code on Curriculum model)
CURRICULUM_EBTEYADI = 'Ebtedayi'
CURRICULUM_DAKHIL = 'Dakhil'
CURRICULUM_SSC = 'SSC'
CURRICULUM_HSC_SCIENCE = 'HSC-Science'
CURRICULUM_HSC_ARTS = 'HSC-Arts'
CURRICULUM_HSC_COMMERCE = 'HSC-Commerce'

# Stream codes (match Stream.code)
STREAM_SCIENCE = 'Science'
STREAM_ARTS = 'Arts'
STREAM_COMMERCE = 'Commerce'

BD_STREAM_CODES = [
    (STREAM_SCIENCE, BD_GROUP_SCIENCE),
    (STREAM_ARTS, BD_GROUP_ARTS),
    (STREAM_COMMERCE, BD_GROUP_COMMERCE),
]

# Level ranges (inclusive)
EBTEYADI_LEVELS = (1, 5)   # Class 1 to 5
DAKHIL_LEVELS = (6, 10)    # Class 6 to 10
SSC_LEVELS = (1, 10)       # Class 1 to 10
HSC_LEVELS = (11, 12)      # Class 11 to 12
