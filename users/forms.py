import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from users.models import User, Student, Instructor


# Registration forms
class StudentRegisterForm(UserCreationForm):

    first_name = forms.CharField(
        label='First Name',
        max_length=50,
        required=True)

    last_name = forms.CharField(
        label='Last Name',
        max_length=50,
        required=True)

    m_initial = forms.CharField(
        label='Middle Initial',
        max_length=1,
        required=False)

    birth_date = forms.DateField(
        label='Date of Birth',
        widget=forms.SelectDateWidget(years=range(1980, 2022)),
        required=True)

    phone_number = forms.CharField(
        label='Phone Number',
        min_length=0,
        max_length=9,
        strip=True,
        required=True)

    street_address = forms.CharField(
        label='Street Address',
        max_length=50,
        required=True)

    city = forms.CharField(
        label='City',
        required=True)

    state = forms.CharField(
        label='State',
        min_length=2,
        max_length=2,
        required=True)

    zip_code = forms.CharField(
        label='Zip Code',
        max_length=5,
        required=True)

    sc_name = forms.CharField(
        label='Previous School Name',
        max_length=50,
        required=False)

    sc_city = forms.CharField(
        label='Previous School City',
        max_length=50,
        required=False)

    sc_state = forms.CharField(
        label='Previous School State',
        min_length=2,
        max_length=2,
        required=False)

    graduation_date = forms.DateField(
        label='Graduation Date',
        widget=forms.SelectDateWidget(years=range(1980, 2030)),
        required=False)

    gpa = forms.FloatField(
        label='GPA',
        min_value=0.0,
        max_value=4.0,
        required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'm_initial', 'last_name', 'email',
                  'birth_date', 'phone_number', 'street_address', 'city', 'state', 'zip_code', 'sc_name',
                  'sc_city', 'sc_state', 'graduation_date', 'gpa']

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')

        if not data.isdigit() or len(data) < 9:
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

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.m_initial = self.cleaned_data.get('m_initial')
        user.email = self.cleaned_data.get('email')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.street_address = self.cleaned_data.get('street_address')
        user.city = self.cleaned_data.get('city').capitalize()
        user.state = self.cleaned_data.get('state').upper()
        user.zip_code = self.cleaned_data.get('zip_code')

        user.is_student = True
        user.save()

        student = Student.objects.create(user=user)
        student.sc_name = self.cleaned_data.get('sc_name')
        student.sc_city = self.cleaned_data.get('sc_city')
        student.sc_state = self.cleaned_data.get('sc_state')
        student.graduation_date = self.cleaned_data.get('graduation_date')
        student.gpa = self.cleaned_data.get('gpa')
        student.save()

        return user


class InstructorRegisterForm(UserCreationForm):
    prefix = "POOP FART"

    first_name = forms.CharField(
        label='First Name',
        max_length=50,
        required=True,
        )

    last_name = forms.CharField(
        label='Last Name',
        max_length=50,
        required=True)

    m_initial = forms.CharField(
        label='Middle Initial',
        max_length=1,
        required=False)

    birth_date = forms.DateField(
        label='Date of Birth',
        widget=forms.SelectDateWidget(years=range(1980, 2022)),
        required=True)

    phone_number = forms.CharField(
        label='Phone Number',
        min_length=0,
        max_length=9,
        strip=True,
        required=True)

    street_address = forms.CharField(
        label='Street Address',
        max_length=50,
        required=True)

    city = forms.CharField(
        label='City',
        required=True)

    state = forms.CharField(
        label='State',
        min_length=2,
        max_length=2,
        required=True)

    zip_code = forms.CharField(
        label='Zip Code',
        max_length=5,
        required=True)

    resume = forms.FileField(
        help_text="Upload a copy of your resume."
    )

    class Meta(UserCreationForm.Meta):
        model = User

        fields = ['username', 'password1', 'password2', 'first_name', 'm_initial', 'last_name', 'email',
                  'birth_date', 'phone_number', 'street_address', 'city', 'state', 'zip_code', 'resume']

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')

        if not data.isdigit() or len(data) < 9:
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

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_instructor = True

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.m_initial = self.cleaned_data.get('m_initial')
        user.email = self.cleaned_data.get('email')
        user.birth_date = self.cleaned_data.get('birth_date')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.street_address = self.cleaned_data.get('street_address')
        user.city = self.cleaned_data.get('city').capitalize()
        user.state = self.cleaned_data.get('state').upper()
        user.zip_code = self.cleaned_data.get('zip_code')

        user.save()

        instructor = Instructor.objects.create(user=user)
        instructor.resume = self.cleaned_data.get('resume')
        instructor.save()

        return user


