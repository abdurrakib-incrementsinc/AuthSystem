from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserInformation, OTPModel
# Register your models here.


class CustomUserAdmin(UserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "id", "email", "username",
        "is_superuser", "is_staff", "is_owner",
        "is_active", "is_manager",
        "date_joined", "last_login"
    ]
    list_filter = ['is_active', 'is_owner', 'is_staff', 'is_superuser', 'is_manager']
    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Login Info", {"fields": ("username", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_active",
                    "is_manager",
                    "is_owner",
                    "groups",
                    "user_permissions",
                    "is_staff",
                )
            },
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", 'username']
    ordering = ["-date_joined"]
    readonly_fields = ("id",)


# Now register the new UserAdmin...
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserInformation)
admin.site.register(OTPModel)

