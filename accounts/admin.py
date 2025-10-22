from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Parent


class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin - Prevents foreign key constraint errors
    Handles deletion of users with related Student/Parent profiles properly
    """
    list_display = [
        "username",
        "email",
        "get_full_name",
        "is_active",
        "is_student",
        "is_lecturer",
        "is_staff",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    list_filter = ['is_active', 'is_student', 'is_lecturer', 'is_staff', 'date_joined']
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'picture')
        }),
        ('User Type', {
            'fields': ('is_student', 'is_lecturer')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_student', 'is_lecturer'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
    
    def delete_model(self, request, obj):
        """
        Override delete to handle related Student/Parent profiles properly
        Prevents circular deletion and FK constraint errors
        """
        try:
            # Delete related profiles first (they have CASCADE to User)
            # This prevents the circular deletion issue
            if hasattr(obj, 'student_profile'):
                # Temporarily override Student's delete method
                obj.student_profile.delete(force=True)
            if hasattr(obj, 'parent_profile'):
                obj.parent_profile.delete()
                
            # Now delete the user safely
            super().delete_model(request, obj)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error deleting user: {str(e)}")
            raise
    
    def delete_queryset(self, request, queryset):
        """
        Override bulk delete to handle related profiles
        """
        try:
            for obj in queryset:
                self.delete_model(request, obj)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error during bulk delete: {str(e)}")
            raise

    class Meta:
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"

class StudentAdmin(admin.ModelAdmin):
    """
    Student/Participant Admin - Manages bootcamp enrollments
    """
    list_display = ['get_student_name', 'get_email', 'level', 'program', 'date_joined']
    list_filter = ['level', 'program', 'student__date_joined']
    search_fields = ['student__username', 'student__email', 'student__first_name', 'student__last_name']
    autocomplete_fields = ['student']
    raw_id_fields = ['student']  # Prevents dropdown foreign key issues
    
    fieldsets = (
        ('Participant Information', {
            'fields': ('student', 'level', 'program')
        }),
    )
    
    def get_student_name(self, obj):
        return obj.student.get_full_name if obj.student else "N/A"
    get_student_name.short_description = 'Student Name'
    get_student_name.admin_order_field = 'student__first_name'
    
    def get_email(self, obj):
        return obj.student.email if obj.student else "N/A"
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'student__email'
    
    def date_joined(self, obj):
        if obj.student:
            return obj.student.date_joined.strftime('%Y-%m-%d %H:%M')
        return "N/A"
    date_joined.short_description = 'Joined Date'
    date_joined.admin_order_field = 'student__date_joined'
    
    def save_model(self, request, obj, form, change):
        """Override save to handle foreign key constraints properly"""
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error saving student: {str(e)}")
            raise
    
    def delete_model(self, request, obj):
        """
        Override delete to handle User deletion properly
        When deleting Student from admin, also delete the User
        """
        try:
            user = obj.student
            # Delete student first (won't try to delete user because of CASCADE)
            super().delete_model(request, obj)
            # Then delete user
            if user:
                user.delete()
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error deleting student: {str(e)}")
            raise
    
    def delete_queryset(self, request, queryset):
        """Override bulk delete for students"""
        try:
            users_to_delete = [obj.student for obj in queryset if obj.student]
            # Delete students first
            queryset.delete()
            # Then delete users
            for user in users_to_delete:
                if user:
                    user.delete()
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Error during bulk delete: {str(e)}")
            raise

# Register bootcamp user models
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
