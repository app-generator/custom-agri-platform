from django import forms
from apps.common.models import Sheet, Role
from apps.users.models import UserRole


class SheetForm(forms.ModelForm):
    class Meta:
        model = Sheet
        # fields = '__all__'
        exclude = ('farm', )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields.pop('state', None)
        else:
            has_permission = False

            if user and user.active_farm:
                has_permission = Role.objects.filter(
                    user=user,
                    farm=user.active_farm,
                    active=True,
                    role__in=[UserRole.FARMER, UserRole.AUDITOR]
                ).exists()

            if not has_permission:
                self.fields.pop('state', None)

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['class'] = (
                'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm '
                'rounded-lg focus:ring-primary-500 focus:border-primary-500 '
                'block w-full p-2.5'
            )

            if field_name == 'info':
                field.widget.attrs['class'] = ''
                field.widget.attrs['rows'] = 8
            
            if field_name == 'file':
                field.widget.attrs['class'] = (
                    'block w-full text-sm text-gray-900 border border-gray-300 '
                    'rounded-lg cursor-pointer bg-gray-50'
                )