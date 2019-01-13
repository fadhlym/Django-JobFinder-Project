from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from mypi import settings

from .models import Profile, kerja

CHOICES = (('', 'Select'), ('Full time', 'Full time'), ('Part time', 'Part time'), ('Freelance', 'Freelance'),)
OPTIONS = (('', 'Select City'), ('Surabaya' ,'Surabaya'), ('Jakarta Timur','Jakarta Timur'), ('Bandung','Bandung'), ('Jakarta Barat','Jakarta Barat'), ('Medan','Medan'), ('Jakarta Selatan','Jakarta Selatan'), ('Bekasi','Bekasi'), ('Tangerang','Tangerang'),
           ('Jakarta Utara','Jakarta Utara'), ('Semarang','Semarang'), ('Depok','Depok'), ('Palembang','Palembang'), ('Tangerang Selatan','Tangerang Selatan'), ('Makassar','Makassar'), ('Batam','Batam'), ('Bogor','Bogor'),
           ('Jakarta Pusat','Jakarta Pusat'),)
GENDER = (('Male','Male'),('Female','Female'))

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,help_text='Required. Enter date as Month-Day-Year')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1']:
            self.fields[fieldname].help_text = 'Required, Obviously'

    class Meta:
        model = User
        fields = ('email','birth_date', 'username', 'password1', 'password2', )


class kerjaForm(forms.ModelForm):
    nama_kerja = forms.CharField(label='Job Name')
    umur = forms.CharField(label='Age Requirements', help_text='in range, ex: a-b')
    gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=GENDER)

    def selected_genders_labels(self):
        return [label for value, label in self.fields['gender'].choices if value in self['gender'].value()]

    sal = forms.CharField(label='Salary',help_text='in Rupiah. Leave it blank if its confidential',widget=forms.NumberInput)
    job_type = forms.ChoiceField(label='Job Type',widget=forms.Select() ,choices=CHOICES)
    kota = forms.ChoiceField(label='City',widget=forms.Select(),choices=OPTIONS)

    def __init__(self, *args, **kwargs):
        super(kerjaForm, self).__init__(*args, **kwargs)

        for fieldname in ['exp']:
            self.fields[fieldname].label = 'Years of Experience'
            self.fields[fieldname].help_text = 'Leave it 0 if Experience is not needed'

        self.fields['sal'].required = False

        for str in ['job_req','jobs_desc','comp_desc']:
            self.fields[str].required = True

        self.fields['job_req'].label = 'Job Requirements'
        self.fields['jobs_desc'].label = 'Job Description'
        self.fields['comp_desc'].label = 'Company Description'

    class Meta:
        model = kerja
        fields = ['nama_kerja', 'umur', 'gender','exp' ,'job_type','job_req', 'jobs_desc', 'sal' , 'comp_name' , 'comp_address', 'comp_sites', 'comp_phone', 'comp_desc', 'kota',]
        exclude = ['user','pub_date',]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('perusahaan', 'location',)