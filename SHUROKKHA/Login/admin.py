from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):#custom class inheriting from django default admin class
 
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'division')}),
    )

  
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Info', {
            'classes': ('wide',), #css
            'fields': ('role', 'division'),
        }),
    )
    list_display = ('id', 'username', 'email', 'role', 'division', 'is_staff', 'is_active') #clumns
    list_filter = ('role', 'division', 'is_active') #dropdwon will show
    search_fields = ('username', 'email', 'division') #can search by this
    def save_model(self, request, obj, form, change):
     if not change:
        obj.set_password('operator123')  # Default password
     super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)