import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.db import transaction
from users.models import User, Instructor, EnrollmentApplication


# applications forms
class StudentApplicationForm(ModelForm):
    first_name = forms.CharField(label='First Name', max_length=50, required=True)
    last_name = forms.CharField(label='Last Name', max_length=50, required=True)
    m_initial = forms.CharField(label='Middle Initial', max_length=1, required=False)
    birth_date = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=range(1980, 2022)), required=True)
    phone_number = forms.CharField(label='Phone Number', min_length=0, max_length=10, strip=True, required=True)
    street_address = forms.CharField(label='Street Address', max_length=50, required=True)
    city = forms.CharField(label='City', required=True)
    state = forms.CharField(label='State', min_length=2, max_length=2, required=True)
    zip_code = forms.CharField(label='Zip Code', max_length=5, required=True)

    sc_name = forms.CharField(label='Previous School Name', max_length=50, required=True)
    sc_city = forms.CharField(label='Previous School City', max_length=50, required=True)
    sc_state = forms.CharField(label='Previous School State', min_length=2, max_length=2, required=True)
    graduation_date = forms.DateField(label='Graduation Date', widget=forms.SelectDateWidget(years=range(1980, 2030)), required=True)
    gpa = forms.FloatField(label='GPA', min_value=0.0, max_value=4.0, required=True)
    transcript = forms.FileField(label='Transcript', required=True, help_text='Upload a copy of your transcript as a .pdf file.')

    class Meta(UserCreationForm.Meta):
        model = EnrollmentApplication
        fields = ['first_name', 'm_initial', 'last_name', 'email',
                  'birth_date', 'phone_number', 'street_address', 'city', 'state', 'zip_code', 'sc_name',
                  'sc_city', 'sc_state', 'graduation_date', 'gpa', 'transcript']

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')

        if not data.isdigit():
            raise forms.ValidationError('Invalid phone number.')

        return data

    def clean_birth_date(self):
        data = self.cleaned_data.get('birth_date')

        if data > datetime.date.today():
            raise forms.ValidationError('Invalid date of birth.')

        return data

    def clean_zip_code(self):
        data = self.cleaned_data.get('zip_code')

        if not data.isdigit() or len(data) != 5:
            raise forms.ValidationError('Invalid zip code.')

        return data

    def clean_email(self):
        data = self.cleaned_data.get('email')

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('User with given email already exists.')

        return data

    def clean_transcript(self):
        data = self.cleaned_data.get('transcript')

        if not data.name.endswith('.pdf'):
            raise forms.ValidationError('Incorrect file format. Please upload a .pdf file.')

        return data

    @transaction.atomic
    def save(self):
        student_application = EnrollmentApplication.objects.create()

        student_application.student_application = True
        student_application.first_name = self.cleaned_data.get('first_name').capitalize()
        student_application.last_name = self.cleaned_data.get('last_name').capitalize()
        student_application.m_initial = self.cleaned_data.get('m_initial').capitalize()
        student_application.email = self.cleaned_data.get('email')
        student_application.birth_date = self.cleaned_data.get('birth_date')
        student_application.phone_number = self.cleaned_data.get('phone_number')
        student_application.street_address = self.cleaned_data.get('street_address')
        student_application.city = self.cleaned_data.get('city').capitalize()
        student_application.state = self.cleaned_data.get('state').upper()
        student_application.zip_code = self.cleaned_data.get('zip_code')
        student_application.sc_name = self.cleaned_data.get('sc_name')
        student_application.sc_city = self.cleaned_data.get('sc_city')
        student_application.sc_state = self.cleaned_data.get('sc_state')
        student_application.graduation_date = self.cleaned_data.get('graduation_date')
        student_application.gpa = self.cleaned_data.get('gpa')
        student_application.transcript = self.cleaned_data.get('transcript')

        student_application.save()

        return student_application


class InstructorApplicationForm(ModelForm):
    first_name = forms.CharField(label='First Name', max_length=50, required=True)
    last_name = forms.CharField(label='Last Name', max_length=50, required=True)
    m_initial = forms.CharField(label='Middle Initial', max_length=1, required=False)
    birth_date = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=range(1980, 2022)), required=True)
    phone_number = forms.CharField(label='Phone Number', min_length=0, max_length=10, strip=True, required=True)
    street_address = forms.CharField(label='Street Address', max_length=50, required=True)
    city = forms.CharField(label='City', required=True)
    state = forms.CharField(label='State', min_length=2, max_length=2, required=True)
    zip_code = forms.CharField(label='Zip Code', max_length=5, required=True)
    resume = forms.FileField(label='Résumé', required=True, help_text='Upload a copy of your résumé as a .pdf file.')

    class Meta(UserCreationForm.Meta):
        model = EnrollmentApplication
        fields = ['first_name', 'm_initial', 'last_name', 'email',
                  'birth_date', 'phone_number', 'street_address', 'city', 'state', 'zip_code', 'resume']

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')

        if not data.isdigit():
            raise forms.ValidationError('Invalid phone number.')

        return data

    def clean_birth_date(self):
        data = self.cleaned_data.get('birth_date')

        if data > datetime.date.today():
            raise forms.ValidationError('Invalid date of birth.')

        return data

    def clean_zip_code(self):
        data = self.cleaned_data.get('zip_code')

        if not data.isdigit() or len(data) != 5:
            raise forms.ValidationError('Invalid zip code.')

        return data

    def clean_resume(self):
        data = self.cleaned_data.get('resume')

        if not data.name.endswith('.pdf'):
            raise forms.ValidationError('Incorrect file format. Please upload a .pdf file.')

        return data

    @transaction.atomic
    def save(self):
        instructor_application = EnrollmentApplication.objects.create()

        instructor_application.Instructor_application = True
        instructor_application.first_name = self.cleaned_data.get('first_name').capitalize()
        instructor_application.last_name = self.cleaned_data.get('last_name').capitalize()
        instructor_application.m_initial = self.cleaned_data.get('m_initial').capitalize()
        instructor_application.email = self.cleaned_data.get('email')
        instructor_application.birth_date = self.cleaned_data.get('birth_date')
        instructor_application.phone_number = self.cleaned_data.get('phone_number')
        instructor_application.street_address = self.cleaned_data.get('street_address')
        instructor_application.city = self.cleaned_data.get('city').capitalize()
        instructor_application.state = self.cleaned_data.get('state').upper()
        instructor_application.zip_code = self.cleaned_data.get('zip_code')
        instructor_application.resume = self.cleaned_data.get('resume')
        instructor_application.save()

        return instructor_application


# registrar decision on enrollment application form
class AcceptApplication(forms.Form):
    DECISION_CHOICES = (
        ('Y', 'Accept'),
        ('N', 'Reject'),
    )

    decision = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=DECISION_CHOICES)
    reason = forms.CharField(label='Justification:', required=False, widget=forms.Textarea, max_length=500, help_text='Max. 500 characters.', initial='')


# Simple login form
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


# User creation form for admin
class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
