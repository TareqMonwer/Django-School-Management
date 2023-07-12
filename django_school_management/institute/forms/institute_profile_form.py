from django import forms

from django_school_management.institute.models import InstituteProfile



class InstituteProfileCreateForm(forms.ModelForm):
    class Meta:
        model = InstituteProfile
        fields = '__all__'
        exclude = ['active', 'created_by']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True, *args, **kwargs):
      if self.request is not None and self.request.user.is_authenticated:
          self.instance.created_by = self.request.user
          self.instance.active = True
      return super().save(commit=commit)

