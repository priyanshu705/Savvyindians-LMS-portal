from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django_filters.views import FilterView

try:
    from allauth.socialaccount.models import SocialAccount
except Exception:
    SocialAccount = None
# to generate pdf from template we need the following
from django.http import HttpResponse
from django.template.loader import (
    render_to_string,
)  # to render a template into a string

from core.models import Semester, Session
from course.models import Course
from result.models import TakenCourse

from .decorators import admin_required
from .filters import LecturerFilter, StudentFilter
from .forms import (
    ParentAddForm,
    ProfileUpdateForm,
    ProgramUpdateForm,
    StaffAddForm,
    StudentAddForm,
    StudentLoginForm,
    StudentRegistrationForm,
)
from .models import Parent, Student, User


def validate_username(request):
    username = request.GET.get("username", None)
    data = {"is_taken": User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)


def register(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        if form.is_valid():
            form.save()
            # no placeholder in string, use normal string instead of f-string
            messages.success(request, "Account created successfuly.")
        else:
            messages.error(
                request,
                "Somthing is not correct, please fill all fields correctly.",
            )
    else:
        form = StudentAddForm(request.POST)
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    """Show profile of any user that fire out the request"""
    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    if request.user.is_lecturer:
        courses = Course.objects.filter(
            allocated_course__lecturer__pk=request.user.id
        ).filter(semester=current_semester)
        return render(
            request,
            "accounts/profile.html",
            {
                "title": request.user.get_full_name,
                "courses": courses,
                "current_session": current_session,
                "current_semester": current_semester,
            },
        )
    elif request.user.is_student:
        level = Student.objects.get(student__pk=request.user.id)
        try:
            parent = Parent.objects.get(student=level)
        except:
            parent = "no parent set"
        courses = TakenCourse.objects.filter(
            student__student__id=request.user.id, course__level=level.level
        )
        context = {
            "title": request.user.get_full_name,
            "parent": parent,
            "courses": courses,
            "level": level,
            "current_session": current_session,
            "current_semester": current_semester,
        }
        return render(request, "accounts/profile.html", context)
    else:
        staff = User.objects.filter(is_lecturer=True)
        return render(
            request,
            "accounts/profile.html",
            {
                "title": request.user.get_full_name,
                "staff": staff,
                "current_session": current_session,
                "current_semester": current_semester,
            },
        )


# function that generate pdf by taking Django template and its context,
def render_to_pdf(template_name, context):
    """Renders a given template to PDF format if xhtml2pdf is available; otherwise returns a friendly message."""
    try:
        from xhtml2pdf import pisa  # Lazy import to avoid serverless dependency issues
    except Exception:
        # Graceful fallback when PDF engine isn't available in the environment
        html = render_to_string(template_name, context)
        return HttpResponse(
            "PDF generation is temporarily unavailable on this deployment.\n\n"
            "You can still view the HTML version below:\n\n" + html,
            content_type="text/html",
        )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="profile.pdf"'  # Set default filename

    template = render_to_string(template_name, context)
    pdf = pisa.CreatePDF(template, dest=response)
    if pdf.err:
        return HttpResponse("We had some problems generating the PDF")

    return response


@login_required
@admin_required
def profile_single(request, id):
    """Show profile of any selected user"""
    if request.user.id == id:
        return redirect("/profile/")

    current_session = Session.objects.filter(is_current_session=True).first()
    current_semester = Semester.objects.filter(
        is_current_semester=True, session=current_session
    ).first()

    user = User.objects.get(pk=id)
    """
    If download_pdf exists, instead of calling render_to_pdf directly, 
    pass the context dictionary built for the specific user type 
    (lecturer, student, or superuser) to the render_to_pdf function.
    """
    if request.GET.get("download_pdf"):
        if user.is_lecturer:
            courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(
                semester=current_semester
            )
            context = {
                "title": user.get_full_name,
                "user": user,
                "user_type": "Lecturer",
                "courses": courses,
                "current_session": current_session,
                "current_semester": current_semester,
            }
        elif user.is_student:
            student = Student.objects.get(student__pk=id)
            courses = TakenCourse.objects.filter(
                student__student__id=id, course__level=student.level
            )
            context = {
                "title": user.get_full_name,
                "user": user,
                "user_type": "student",
                "courses": courses,
                "student": student,
                "current_session": current_session,
                "current_semester": current_semester,
            }
        else:
            context = {
                "title": user.get_full_name,
                "user": user,
                "user_type": "superuser",
                "current_session": current_session,
                "current_semester": current_semester,
            }
        return render_to_pdf("pdf/profile_single.html", context)

    else:
        if user.is_lecturer:
            courses = Course.objects.filter(allocated_course__lecturer__pk=id).filter(
                semester=current_semester
            )
            context = {
                "title": user.get_full_name,
                "user": user,
                "user_type": "Lecturer",
                "courses": courses,
                "current_session": current_session,
                "current_semester": current_semester,
            }
            return render(request, "accounts/profile_single.html", context)
        elif user.is_student:
            student = Student.objects.get(student__pk=id)
            courses = TakenCourse.objects.filter(
                student__student__id=id, course__level=student.level
            )
            context = {
                "title": user.get_full_name,
                "user": user,
                "user_type": "student",
                "courses": courses,
                "student": student,
                "current_session": current_session,
                "current_semester": current_semester,
            }
            return render(request, "accounts/profile_single.html", context)
        else:
            context = {
                "title": user.get_full_name,
                "user": user,
                "user_type": "superuser",
                "current_session": current_session,
                "current_semester": current_semester,
            }
            return render(request, "accounts/profile_single.html", context)


@login_required
@admin_required
def admin_panel(request):
    return render(
        request, "setting/admin_panel.html", {"title": request.user.get_full_name}
    )


# ########################################################


# ########################################################
# Setting views
# ########################################################
@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(
        request,
        "setting/profile_info_change.html",
        {
            "title": "Setting",
            "form": form,
        },
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the error(s) below. ")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "setting/password_change.html",
        {
            "form": form,
        },
    )


# ########################################################


@login_required
@admin_required
def staff_add_view(request):
    if request.method == "POST":
        form = StaffAddForm(request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if form.is_valid():

            form.save()
            messages.success(
                request,
                "Account for lecturer "
                + first_name
                + " "
                + last_name
                + " has been created. An email with account credentials will be sent to "
                + email
                + " within a minute.",
            )
            return redirect("lecturer_list")
    else:
        form = StaffAddForm()

    context = {
        "title": "Lecturer Add",
        "form": form,
    }

    return render(request, "accounts/add_staff.html", context)


@login_required
@admin_required
def edit_staff(request, pk):
    instance = get_object_or_404(User, is_lecturer=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, "Lecturer " + full_name + " has been updated.")
            return redirect("lecturer_list")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(
        request,
        "accounts/edit_lecturer.html",
        {
            "title": "Edit Lecturer",
            "form": form,
        },
    )


@method_decorator([login_required, admin_required], name="dispatch")
class LecturerFilterView(FilterView):
    filterset_class = LecturerFilter
    queryset = User.objects.filter(is_lecturer=True)
    template_name = "accounts/lecturer_list.html"
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Lecturers"
        return context


# lecturers list pdf
def render_lecturer_pdf_list(request):
    lecturers = User.objects.filter(is_lecturer=True)
    template_path = "pdf/lecturer_list.html"
    context = {"lecturers": lecturers}
    return render_to_pdf(template_path, context)


# @login_required
# @lecturer_required
# def delete_staff(request, pk):
#     staff = get_object_or_404(User, pk=pk)
#     staff.delete()
#     return redirect('lecturer_list')


@login_required
@admin_required
def delete_staff(request, pk):
    lecturer = get_object_or_404(User, pk=pk)
    full_name = lecturer.get_full_name
    lecturer.delete()
    messages.success(request, "Lecturer " + full_name + " has been deleted.")
    return redirect("lecturer_list")


# ########################################################


# ########################################################
# Student views
# ########################################################
@login_required
@admin_required
def student_add_view(request):
    if request.method == "POST":
        form = StudentAddForm(request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account for "
                + first_name
                + " "
                + last_name
                + " has been created. An email with account credentials will be sent to "
                + email
                + " within a minute.",
            )
            return redirect("student_list")
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = StudentAddForm()

    return render(
        request,
        "accounts/add_student.html",
        {"title": "Add Student", "form": form},
    )


@login_required
@admin_required
def edit_student(request, pk):
    # instance = User.objects.get(pk=pk)
    instance = get_object_or_404(User, is_student=True, pk=pk)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = instance.get_full_name
        if form.is_valid():
            form.save()

            messages.success(request, ("Student " + full_name + " has been updated."))
            return redirect("student_list")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = ProfileUpdateForm(instance=instance)
    return render(
        request,
        "accounts/edit_student.html",
        {
            "title": "Edit-profile",
            "form": form,
        },
    )


@method_decorator([login_required, admin_required], name="dispatch")
class StudentListView(FilterView):
    queryset = Student.objects.all()
    filterset_class = StudentFilter
    template_name = "accounts/student_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Students"
        return context


# student list pdf
def render_student_pdf_list(request):
    students = Student.objects.all()
    template_path = "pdf/student_list.html"
    context = {"students": students}
    return render_to_pdf(template_path, context)


@login_required
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # full_name = student.user.get_full_name
    student.delete()
    messages.success(request, "Student has been deleted.")
    return redirect("student_list")


@login_required
@admin_required
def edit_student_program(request, pk):

    instance = get_object_or_404(Student, student_id=pk)
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = ProgramUpdateForm(request.POST, request.FILES, instance=instance)
        full_name = user.get_full_name
        if form.is_valid():
            form.save()
            messages.success(request, message=full_name + " program has been updated.")
            url = (
                "/accounts/profile/" + user.id.__str__() + "/detail/"
            )  # Botched job, must optimize
            return redirect(to=url)
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = ProgramUpdateForm(instance=instance)
    return render(
        request,
        "accounts/edit_student_program.html",
        context={"title": "Edit-program", "form": form, "student": instance},
    )


# ########################################################


class ParentAdd(CreateView):
    model = Parent
    form_class = ParentAddForm
    template_name = "accounts/parent_form.html"


# def parent_add(request):
#     if request.method == 'POST':
#         form = ParentAddForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')
#     else:
#         form = ParentAddForm(request.POST)


# ########################################################
# Student Authentication Views
# ########################################################


def student_login(request):
    """Enhanced login view specifically for students"""
    if request.user.is_authenticated:
        if hasattr(request.user, "is_student") and request.user.is_student:
            return redirect("user_course_list")
        else:
            messages.info(request, _("Please use the student login form."))
            logout(request)

    if request.method == "POST":
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Set session expiry based on remember_me
            if form.cleaned_data.get("remember_me"):
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
            else:
                request.session.set_expiry(60 * 60 * 8)  # 8 hours

            login(request, user)
            messages.success(request, _("Welcome back, {}!".format(user.get_full_name)))

            # Redirect to next URL or default student dashboard
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect("user_course_list")
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = StudentLoginForm()

    context = {
        "form": form,
        "title": _("Student Login"),
    }
    return render(request, "accounts/student_login.html", context)


def student_register(request):
    """Enhanced registration view for bootcamp/masterclass participants"""
    if request.user.is_authenticated:
        messages.info(request, _("You are already logged in."))
        return redirect("user_course_list")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                _(
                    "Welcome to the bootcamp! You can now login with your email: {}"
                ).format(user.email),
            )
            return redirect("student_login")
        else:
            messages.error(request, _("Please correct the errors below."))
    else:
        form = StudentRegistrationForm()

    context = {
        "form": form,
        "title": _("Join AI Bootcamp"),
    }
    return render(request, "accounts/student_register_bootcamp.html", context)


def student_logout(request):
    """Enhanced logout view for students with OAuth support"""
    if request.user.is_authenticated:
        user_name = (
            request.user.get_full_name
            if hasattr(request.user, "get_full_name")
            else str(request.user)
        )

        # Check if user has OAuth social accounts
        social_accounts = (
            SocialAccount.objects.filter(user=request.user) if SocialAccount else []
        )
        has_google_account = (
            social_accounts.filter(provider="google").exists()
            if SocialAccount
            else False
        )

        # Store user info for logout confirmation page
        context = {
            "user_name": user_name,
            "has_google_account": has_google_account,
            "social_accounts": social_accounts,
        }

        # If GET request, show logout confirmation page
        if request.method == "GET":
            return render(request, "accounts/logout_confirm.html", context)

        # If POST request, perform logout
        elif request.method == "POST":
            # Clear all sessions and logout
            logout(request)

            # Add appropriate success message
            if has_google_account:
                messages.success(
                    request,
                    _(
                        "You have been logged out successfully from both your student account and Google. See you next time, {}!"
                    ).format(user_name),
                )
            else:
                messages.success(
                    request,
                    _(
                        "You have been logged out successfully. See you next time, {}!"
                    ).format(user_name),
                )

            # Redirect to home page after logout
            return redirect("home")

    # If user is not authenticated, redirect to home page
    return redirect("home")


@login_required
def oauth_connections(request):
    """View for managing OAuth social account connections"""
    social_accounts = (
        SocialAccount.objects.filter(user=request.user) if SocialAccount else []
    )

    context = {
        "title": _("Connected Accounts"),
        "social_accounts": social_accounts,
        "has_google_account": (
            social_accounts.filter(provider="google").exists()
            if SocialAccount
            else False
        ),
        "user": request.user,
    }
    return render(request, "accounts/oauth_connections.html", context)


def lecturer_login(request):
    """Enhanced login view specifically for lecturers/instructors"""
    if request.user.is_authenticated:
        if hasattr(request.user, "is_lecturer") and request.user.is_lecturer:
            return redirect("admin_panel")
        else:
            messages.info(request, _("Please use the lecturer login form."))
            logout(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if hasattr(user, "is_lecturer") and user.is_lecturer:
                login(request, user)
                messages.success(
                    request, _("Welcome back, {}!".format(user.get_full_name))
                )

                # Redirect to next URL or default lecturer dashboard
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("admin_panel")
            else:
                messages.error(
                    request, _("This account is not registered as a lecturer.")
                )
        else:
            messages.error(request, _("Invalid username or password."))

    context = {
        "title": _("Lecturer Login"),
    }
    return render(request, "accounts/lecturer_login.html", context)
