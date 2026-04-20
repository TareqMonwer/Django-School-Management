"""
Education boards library: country-based boards for admission forms.

Bangladesh (BD) boards are used for both polytechnic and school/madrasah admission.
Other countries can add boards via the database (EducationBoard model) or keep
free-text board field for backward compatibility.
"""

# Bangladesh ISO 3166-1 alpha-2
COUNTRY_BD = 'BD'

# Bangladesh education boards (name as shown in dropdown)
# Order matches common usage; code can be used for display or reporting.
BD_BOARDS = [
    ('Dhaka Board (BISE, Dhaka)', 'Dhaka'),
    ('Rajshahi Board', 'Rajshahi'),
    ('Cumilla Board', 'Cumilla'),
    ('Jessore Board', 'Jessore'),
    ('Chittagong Board', 'Chittagong'),
    ('Barisal Board', 'Barisal'),
    ('Sylhet Board', 'Sylhet'),
    ('Dinajpur Board', 'Dinajpur'),
    ('Mymensingh Board', 'Mymensingh'),
    ('Bangladesh Madrasah Education Board', 'Madrasah'),
]

# BD group choices for polytechnic (SSC/HSC style)
BD_GROUP_SCIENCE = 'Science'
BD_GROUP_ARTS = 'Arts'
BD_GROUP_COMMERCE = 'Commerce'

BD_GROUPS = [
    (BD_GROUP_SCIENCE, BD_GROUP_SCIENCE),
    (BD_GROUP_ARTS, BD_GROUP_ARTS),
    (BD_GROUP_COMMERCE, BD_GROUP_COMMERCE),
]

# Class levels for school/madrasah (e.g. 1-10); JSC/JDC exam section shown for 9-10 only
APPLYING_FOR_CLASS_MIN = 1
APPLYING_FOR_CLASS_MAX = 10
APPLYING_FOR_CLASS_JSC_START = 9  # Show JSC/JDC fields when applying_for_class >= this
