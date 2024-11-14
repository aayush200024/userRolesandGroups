from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .forms import UserForm, GroupForm, ExistingGroupForm, PermissionForm
from .models import CustomUser, CustomGroup, CustomPermission

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def manage_users_and_groups(request):
    # Retrieve users, groups, and permissions
    users = CustomUser.objects.all()
    groups = CustomGroup.objects.all()  # Use CustomGroup instead of the default Group
    system_permissions = CustomPermission.objects.filter(content_type__app_label='auth')  # System permissions
    custom_permissions = CustomPermission.objects.exclude(content_type__app_label='auth')  # Custom permissions

    # Initialize forms
    user_form = UserForm()
    group_form = GroupForm()
    existing_group_form = ExistingGroupForm()
    permission_form = PermissionForm()

    if request.method == 'POST':
        # Handle user creation
        if 'add_user' in request.POST:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "User added successfully.")
                return redirect('manage_users_and_groups')

        # Handle custom group creation with selected permissions
        elif 'add_custom_group' in request.POST:
            group_form = GroupForm(request.POST)
            if group_form.is_valid():
                group = group_form.save()
                messages.success(request, "Custom group created successfully.")
                return redirect('manage_users_and_groups')

        # Handle adding existing group to a user
        elif 'add_existing_group' in request.POST:
            existing_group_form = ExistingGroupForm(request.POST)
            if existing_group_form.is_valid():
                group = existing_group_form.cleaned_data['group']
                messages.success(request, f"Existing group '{group.name}' assigned successfully.")
                return redirect('manage_users_and_groups')

        # Handle custom permission creation
        elif 'add_custom_permission' in request.POST:
            permission_form = PermissionForm(request.POST)
            if permission_form.is_valid():
                permission = permission_form.save(commit=False)
                permission.content_type = ContentType.objects.get_for_model(CustomUser)  # Associate with CustomUser
                permission.save()
                messages.success(request, "Custom permission created successfully.")
                return redirect('manage_users_and_groups')

        # Handle updating a user's groups and permissions
        elif 'edit_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(CustomUser, id=user_id)
            selected_groups = request.POST.getlist('groups')
            selected_permissions = request.POST.getlist('permissions')

            # Update the user's groups
            user.groups.clear()
            user.groups.set(CustomGroup.objects.filter(id__in=selected_groups))

            # Update the user's permissions
            user.user_permissions.clear()
            user.user_permissions.set(CustomPermission.objects.filter(id__in=selected_permissions))

            messages.success(request, f"Updated groups and permissions for user '{user.username}' successfully.")
            return redirect('manage_users_and_groups')

    return render(request, 'manage_users_and_groups.html', {
        'users': users,
        'groups': groups,
        'system_permissions': system_permissions,
        'custom_permissions': custom_permissions,
        'user_form': user_form,
        'group_form': group_form,
        'existing_group_form': existing_group_form,
        'permission_form': permission_form,
    })
