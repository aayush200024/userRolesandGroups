from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser, CustomPermission, CustomGroup

# Form to create/edit a user
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    role = forms.ChoiceField(
        choices=[('admin', 'Admin'), ('manager', 'Manager'), ('user', 'User')],
        required=True,
        label="Role"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

# Form to create/edit a custom group with selected custom permissions
class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=CustomPermission.objects.all(),  # Use the custom permissions model
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Custom Permissions"
    )

    class Meta:
        model = CustomGroup
        fields = ['name', 'permissions']

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
            group.permissions.set(self.cleaned_data['permissions'])
        return group

# Form to select an existing custom group to assign to a user
class ExistingGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=CustomGroup.objects.all(),
        required=True,
        label="Select Existing Group"
    )

# Form to create custom permissions
class PermissionForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        label="Permission Name"
    )
    codename = forms.CharField(
        max_length=100,
        required=True,
        label="Permission Codename"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Permission Description"
    )

    class Meta:
        model = CustomPermission  # Use custom permission model
        fields = ['name', 'codename', 'description']

    def save(self, commit=True):
        permission = super().save(commit=False)
        if commit:
            permission.save()
        return permission
