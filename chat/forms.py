from django.forms import ModelForm, TextInput, Textarea
from .models import Report
from django import forms


# Create your forms here.
# creating the django report form automatically
class NewReportForm(forms.ModelForm):

	class Meta:
		model = Report
		fields = ('security_guard', 'assigned_area', 'location', 'category', 'description')

	# scc styling to repot form entries
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['security_guard'].widget.attrs['class'] = 'form-control'
		self.fields['assigned_area'].widget.attrs['class'] = 'form-control'
		self.fields['location'].widget.attrs['class'] = 'form-control'
		self.fields['category'].widget.attrs['class'] = 'form-control'
		self.fields['description'].widget.attrs['class'] = 'form-control'

	# cleaning entries after saving
	def save(self, commit=True):
		report = super(NewReportForm, self).save(commit=False)
		report.security_guard = self.cleaned_data['security_guard']
		report.assigned_area=self.cleaned_data['assigned_area']
		report.location=self.cleaned_data['location']
		report.category=self.cleaned_data['category']
		report.description=self.cleaned_data['description']

		if commit:
			report.save()
		return report
