from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import render_lecturer_pdf_list  # new
from .views import render_student_pdf_list  # new
from .views import (
    LecturerFilterView,
    ParentAdd,
    StudentListView,
    admin_panel,
    change_password,
    delete_staff,
    delete_student,
    edit_staff,
    edit_student,
    edit_student_program,
    lecturer_login,
    oauth_connections,
    profile,
    profile_single,
    profile_update,
    register,
    staff_add_view,
    student_add_view,
    student_login,
    student_logout,
    student_register,
    validate_username,
)

# from .forms import EmailValidationOnForgotPassword


urlpatterns = [
    # Password Reset URLs with custom templates
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("", include("django.contrib.auth.urls")),
    path("admin_panel/", admin_panel, name="admin_panel"),
    path("profile/", profile, name="profile"),
    path("profile/<int:id>/detail/", profile_single, name="profile_single"),
    path("setting/", profile_update, name="edit_profile"),
    path("change_password/", change_password, name="change_password"),
    path("lecturers/", LecturerFilterView.as_view(), name="lecturer_list"),
    path("lecturer/add/", staff_add_view, name="add_lecturer"),
    path("staff/<int:pk>/edit/", edit_staff, name="staff_edit"),
    path("lecturers/<int:pk>/delete/", delete_staff, name="lecturer_delete"),
    path("students/", StudentListView.as_view(), name="student_list"),
    path("student/add/", student_add_view, name="add_student"),
    path("student/<int:pk>/edit/", edit_student, name="student_edit"),
    path("students/<int:pk>/delete/", delete_student, name="student_delete"),
    path(
        "edit_student_program/<int:pk>/",
        edit_student_program,
        name="student_program_edit",
    ),
    path("parents/add/", ParentAdd.as_view(), name="add_parent"),
    path("ajax/validate-username/", validate_username, name="validate_username"),
    path("register/", register, name="register"),
    # Student Authentication URLs
    path("student/login/", student_login, name="student_login"),
    path("student/register/", student_register, name="student_register"),
    path("student/logout/", student_logout, name="student_logout"),
    # Lecturer Authentication URLs
    path("lecturer/login/", lecturer_login, name="lecturer_login"),
    path("oauth/connections/", oauth_connections, name="oauth_connections"),
    # paths to pdf
    path(
        "create_lecturers_pdf_list/", render_lecturer_pdf_list, name="lecturer_list_pdf"
    ),  # new
    path(
        "create_students_pdf_list/", render_student_pdf_list, name="student_list_pdf"
    ),  # new
    # path('add-student/', StudentAddView.as_view(), name='add_student'),
    # path('programs/course/delete/<int:pk>/', course_delete, name='delete_course'),
    # Setting urls
    # path('profile/<int:pk>/edit/', profileUpdateView, name='edit_profile'),
    # path('profile/<int:pk>/change-password/', changePasswordView, name='change_password'),
    # ################################################################
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
    # path('password-reset/', PasswordResetView.as_view(
    #     form_class=EmailValidationOnForgotPassword,
    #     template_name='registration/password_reset.html'
    # ),
    #      name='password_reset'),
    # path('password-reset/done/', PasswordResetDoneView.as_view(
    #     template_name='registration/password_reset_done.html'
    # ),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    #     template_name='registration/password_reset_confirm.html'
    # ),
    #      name='password_reset_confirm'),
    # path('password-reset-complete/', PasswordResetCompleteView.as_view(
    #     template_name='registration/password_reset_complete.html'
    # ),
    #      name='password_reset_complete')
    # ################################################################
]
