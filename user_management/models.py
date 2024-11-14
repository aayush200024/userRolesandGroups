from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Custom user model inheriting from AbstractUser
class CustomUser(AbstractUser):
    # Override groups and user_permissions to avoid conflict with Django's User model
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Changed related_name to avoid conflicts
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Changed related_name to avoid conflicts
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('manager', 'Manager'), ('user', 'User')])

    def __str__(self):
        return self.username


# Custom Permissions model (SrsPermissions or CustomPermission)
class CustomPermission(models.Model):  # This aligns with the naming you're using in views/forms
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    codename = models.CharField(max_length=100)
    django_permission = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'custom_permissions'
        permissions = (
            ("create_permission", "Can create custom permission"),
            ("update_permission", "Can update custom permission"),
            ("read_permission", "Can read custom permission"),
            ("delete_permission", "Can delete custom permission"),
        )

    def __str__(self):
        return self.name


# Custom Group model (SrsGroup or CustomGroup)
class CustomGroup(models.Model):  # Aligned with the CustomGroup name you're using
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = 'custom_groups'
        permissions = (
            ("create_group", "Can create group"),
            ("update_group", "Can update group"),
            ("read_group", "Can read group"),
            ("delete_group", "Can delete group"),
        )

    def __str__(self):
        return self.name


# Group Permissions relationship model
class CustomGroupPermissions(models.Model):
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey(CustomPermission, on_delete=models.CASCADE)
    django_permission = models.ForeignKey(Permission, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'custom_group_permissions'
        unique_together = (('group', 'permission'),)
        permissions = (
            ("create_group_permission", "Can create group permission"),
            ("update_group_permission", "Can update group permission"),
            ("read_group_permission", "Can read group permission"),
            ("delete_group_permission", "Can delete group permission"),
        )

    def __str__(self):
        return f"{self.group.name} - {self.permission.name}"
