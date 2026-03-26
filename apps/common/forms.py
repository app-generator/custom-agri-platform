from django import forms
from apps.common.models import Sheet


class SheetForm(forms.ModelForm):
    class Meta:
        model = Sheet
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(SheetForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'

            if field_name == 'info':
                self.fields[field_name].widget.attrs['class'] = ''
                self.fields[field_name].widget.attrs['rows'] = 8
            
            if field_name == 'file':
                self.fields[field_name].widget.attrs['class'] = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'