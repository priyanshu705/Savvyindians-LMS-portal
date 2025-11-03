from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.core.mail import send_mail
import os

from accounts.decorators import admin_required, lecturer_required
from accounts.models import Student, User

from .forms import NewsAndEventsForm, SemesterForm, SessionForm
from .models import ActivityLog, NewsAndEvents, Semester, Session
from .utils import (
    handle_delete_operation,
    handle_form_submission,
    validate_current_semester_deletion,
    validate_current_session_deletion,
)


# ########################################################
# SavvyIndians AI Bootcamp & Masterclass Homepage
# ########################################################
def home_view(request):
    """Public homepage for SavvyIndians AI Bootcamp & Masterclass platform"""
    from accounts.models import User
    from course.models import Course, Program, UploadVideo

    # Get featured courses and videos for public viewing
    featured_courses = Course.objects.all()[:6]
    featured_videos = UploadVideo.objects.all().order_by("-timestamp")[:8]
    latest_courses = Course.objects.all().order_by("-pk")[:4]

    # Get statistics for hero section
    total_bootcamps = Program.objects.count()
    total_courses = Course.objects.count()
    total_participants = User.objects.filter(is_student=True).count()
    total_videos = UploadVideo.objects.count()

    # Check if user is authenticated
    user_authenticated = request.user.is_authenticated

    context = {
        "title": "SavvyIndians - AI Bootcamps & Masterclasses",
        "featured_courses": featured_courses,
        "featured_videos": featured_videos,
        "latest_courses": latest_courses,
        "total_bootcamps": total_bootcamps,
        "total_courses": total_courses,
        "total_participants": total_participants,
        "total_videos": total_videos,
        "user_authenticated": user_authenticated,
    }
    return render(request, "core/bootcamp_home.html", context)


@login_required
@admin_required
def dashboard_view(request):
    logs = ActivityLog.objects.all().order_by("-created_at")[:10]
    gender_count = Student.get_gender_count()
    context = {
        "student_count": User.objects.get_student_count(),
        "lecturer_count": User.objects.get_lecturer_count(),
        "superuser_count": User.objects.get_superuser_count(),
        "males_count": gender_count["M"],
        "females_count": gender_count["F"],
        "logs": logs,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def post_add(request):
    return handle_form_submission(
        request=request,
        form_class=NewsAndEventsForm,
        template_name="core/post_add.html",
        success_url="home",
        success_message="{title} has been uploaded.",
        context={"title": "Add Post"},
    )


@login_required
@lecturer_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    return handle_form_submission(
        request=request,
        form_class=NewsAndEventsForm,
        template_name="core/post_add.html",
        success_url="home",
        success_message="{title} has been updated.",
        context={"title": "Edit Post"},
        instance=instance,
    )


@login_required
@lecturer_required
def delete_post(request, pk):
    return handle_delete_operation(
        request=request,
        model_class=NewsAndEvents,
        pk_field=pk,
        redirect_url="home",
        success_message="{title} has been deleted.",
    )


# ########################################################
# Session
# ########################################################
@login_required
@lecturer_required
def session_list_view(request):
    """Show list of all sessions"""
    sessions = Session.objects.all().order_by("-is_current_session", "-session")
    return render(request, "core/session_list.html", {"sessions": sessions})


@login_required
@lecturer_required
def session_add_view(request):
    """check request method, if POST we add session otherwise show empty form"""
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            data = form.data.get(
                "is_current_session"
            )  # returns string of 'True' if the user selected Yes
            print(data)
            if data == "true":
                sessions = Session.objects.all()
                if sessions:
                    for session in sessions:
                        if session.is_current_session == True:
                            unset = Session.objects.get(is_current_session=True)
                            unset.is_current_session = False
                            unset.save()
                    form.save()
                else:
                    form.save()
            else:
                form.save()
            messages.success(request, "Session added successfully. ")
            return redirect("session_list")

    else:
        form = SessionForm()
    return render(request, "core/session_update.html", {"form": form})


@login_required
@lecturer_required
def session_update_view(request, pk):
    session = Session.objects.get(pk=pk)
    if request.method == "POST":
        form = SessionForm(request.POST, instance=session)
        data = form.data.get("is_current_session")
        if data == "true":
            sessions = Session.objects.all()
            if sessions:
                for session in sessions:
                    if session.is_current_session == True:
                        unset = Session.objects.get(is_current_session=True)
                        unset.is_current_session = False
                        unset.save()

            if form.is_valid():
                form.save()
                messages.success(request, "Session updated successfully. ")
                return redirect("session_list")
        else:
            form = SessionForm(request.POST, instance=session)
            if form.is_valid():
                form.save()
                messages.success(request, "Session updated successfully. ")
                return redirect("session_list")

    else:
        form = SessionForm(instance=session)
    return render(request, "core/session_update.html", {"form": form})


@login_required
@lecturer_required
def session_delete_view(request, pk):
    return handle_delete_operation(
        request=request,
        model_class=Session,
        pk_field=pk,
        redirect_url="session_list",
        success_message="Session successfully deleted",
        validation_func=validate_current_session_deletion,
    )


# ########################################################


# ########################################################
# Semester
# ########################################################
@login_required
@lecturer_required
def semester_list_view(request):
    semesters = Semester.objects.all().order_by("-is_current_semester", "-semester")
    return render(
        request,
        "core/semester_list.html",
        {
            "semesters": semesters,
        },
    )


@login_required
@lecturer_required
def semester_add_view(request):
    if request.method == "POST":
        form = SemesterForm(request.POST)
        if form.is_valid():
            data = form.data.get(
                "is_current_semester"
            )  # returns string of 'True' if the user selected Yes
            if data == "True":
                semester = form.data.get("semester")
                ss = form.data.get("session")
                session = Session.objects.get(pk=ss)
                try:
                    if Semester.objects.get(semester=semester, session=ss):
                        messages.error(
                            request,
                            semester
                            + " semester in "
                            + session.session
                            + " session already exist",
                        )
                        return redirect("add_semester")
                except:
                    semesters = Semester.objects.all()
                    sessions = Session.objects.all()
                    if semesters:
                        for semester in semesters:
                            if semester.is_current_semester == True:
                                unset_semester = Semester.objects.get(
                                    is_current_semester=True
                                )
                                unset_semester.is_current_semester = False
                                unset_semester.save()
                        for session in sessions:
                            if session.is_current_session == True:
                                unset_session = Session.objects.get(
                                    is_current_session=True
                                )
                                unset_session.is_current_session = False
                                unset_session.save()

                    new_session = request.POST.get("session")
                    set_session = Session.objects.get(pk=new_session)
                    set_session.is_current_session = True
                    set_session.save()
                    form.save()
                    messages.success(request, "Semester added successfully.")
                    return redirect("semester_list")

            form.save()
            messages.success(request, "Semester added successfully. ")
            return redirect("semester_list")
    else:
        form = SemesterForm()
    return render(request, "core/semester_update.html", {"form": form})


@login_required
@lecturer_required
def semester_update_view(request, pk):
    semester = Semester.objects.get(pk=pk)
    if request.method == "POST":
        if (
            request.POST.get("is_current_semester") == "True"
        ):  # returns string of 'True' if the user selected yes for 'is current semester'
            unset_semester = Semester.objects.get(is_current_semester=True)
            unset_semester.is_current_semester = False
            unset_semester.save()
            unset_session = Session.objects.get(is_current_session=True)
            unset_session.is_current_session = False
            unset_session.save()


# ########################################################
# Staff Self-Test Page (Email + Static + Media)
# ########################################################
@staff_member_required
def self_test_view(request):
    """Staff-only page to validate email sending and static/media availability."""
    static_path = finders.find("admin/css/base.css")
    static_ok = bool(static_path)

    media_root_exists = os.path.isdir(settings.MEDIA_ROOT) if settings.MEDIA_ROOT else False
    # Check a couple of common subfolders if present (non-fatal)
    media_subdirs = [
        os.path.join(settings.MEDIA_ROOT, "profile_pictures") if settings.MEDIA_ROOT else None,
        os.path.join(settings.MEDIA_ROOT, "registration_form") if settings.MEDIA_ROOT else None,
    ]
    media_hint = [d for d in media_subdirs if d and os.path.isdir(d)]

    sent_ok = None
    error_msg = None
    if request.method == "POST" and request.POST.get("action") == "send_email":
        recipient = request.user.email or settings.EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL
        try:
            send_mail(
                subject="Self-Test: Email Connectivity",
                message="This is a self-test email from the LMS portal.",
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                fail_silently=False,
            )
            sent_ok = True
            messages.success(request, f"Test email sent to {recipient}")
        except Exception as e:
            sent_ok = False
            error_msg = str(e)
            messages.error(request, f"Email sending failed: {e}")

    context = {
        "static_ok": static_ok,
        "static_path": static_path,
        "media_root": settings.MEDIA_ROOT,
        "media_root_exists": media_root_exists,
        "media_hint": media_hint,
        "email_sender": settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
        "email_recipient": request.user.email,
        "email_result": sent_ok,
        "email_error": error_msg,
    }
    return render(request, "health/self_test.html", context)


@login_required
@lecturer_required
def semester_delete_view(request, pk):
    return handle_delete_operation(
        request=request,
        model_class=Semester,
        pk_field=pk,
        redirect_url="semester_list",
        success_message="Semester successfully deleted",
        validation_func=validate_current_semester_deletion,
    )
