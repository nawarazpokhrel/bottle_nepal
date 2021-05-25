from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from apps.users.models import User, SubscribeEmail


class BaseUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email'
    )
    search_fields = (
        'id',
        'email',
        'username'
    )
    list_display_links = ('id',)

    list_filter = (
        'is_active',
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    ordering = ('-date_joined',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'email',
        )}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',

            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(SubscribeEmail)
class SubscribeEmailAdmin(admin.ModelAdmin):
    list_display = ('user','id',)
    list_display_links = ('id', 'user')
