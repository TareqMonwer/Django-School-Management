from .models import Student
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (Layout, Fieldset, Field,
                                 ButtonHolder, Submit, Div)


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'photo',
            'date_of_birth',
            'roll',
            'registration_number',
            'department',
            'semester',
            'ac_session',
            'mobile',
            'guardian_mobile',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            TabHolder(
                Tab('Personal Info',
                    'name',
                    'photo',
                    'date_of_birth',
                    'email',
                    'mobile',
                    'guardian_mobile',
                    ),
                Tab('Departmental Info',
                    Field('department', css_class="extra"),
                    Field('semester',),
                    Field('ac_session',)
                    ),
                Tab('Board Info',
                    Field('roll', css_class="extra"),
                    Field('registration_number',),
                    )
            ),
            ButtonHolder(
                Submit('submit', 'Admit Student',
                       css_class='float-right btn-dark mr-3')
            )
        )
