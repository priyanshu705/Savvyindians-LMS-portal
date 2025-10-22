from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Q
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# project import
from .utils import *
from core.models import ActivityLog

# Bootcamp Experience Levels (matching accounts.models)
BEGINNER = _("Beginner")
INTERMEDIATE = _("Intermediate")
ADVANCED = _("Advanced")
EXPERT = _("Expert")

LEVEL = (
    (BEGINNER, _("Beginner - New to technology")),
    (INTERMEDIATE, _("Intermediate - Some experience")),
    (ADVANCED, _("Advanced - Strong knowledge")),
    (EXPERT, _("Expert - Industry professional")),
)

# Bootcamp Modules (replacing semesters)
MODULE_ONE = _("Module 1")
MODULE_TWO = _("Module 2")
MODULE_THREE = _("Module 3")
MODULE_FOUR = _("Module 4")
MODULE_FIVE = _("Module 5")

BOOTCAMP_MODULE = (
    (MODULE_ONE, _("Module 1 - Introduction")),
    (MODULE_TWO, _("Module 2 - Fundamentals")),
    (MODULE_THREE, _("Module 3 - Intermediate")),
    (MODULE_FOUR, _("Module 4 - Advanced")),
    (MODULE_FIVE, _("Module 5 - Capstone Project")),
)

# Bootcamp Duration Options (in weeks)
DURATION_CHOICES = (
    (4, _("4 Weeks - Quick Start")),
    (8, _("8 Weeks - Standard")),
    (12, _("12 Weeks - Comprehensive")),
    (16, _("16 Weeks - In-Depth")),
    (24, _("24 Weeks - Master Program")),
)


class ProgramManager(models.Manager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = Q(title__icontains=query) | Q(summary__icontains=query)
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset


class Program(models.Model):
    """
    Bootcamp Program Model
    Represents main bootcamp programs (e.g., 'AI & Machine Learning Bootcamp')
    """
    title = models.CharField(
        max_length=150, 
        unique=True,
        verbose_name=_("Bootcamp Name"),
        help_text=_("Name of the bootcamp program (e.g., 'AI & Machine Learning Bootcamp')")
    )
    summary = models.TextField(
        null=True, 
        blank=True,
        verbose_name=_("Bootcamp Description"),
        help_text=_("Detailed description of what participants will learn")
    )
    
    # Bootcamp-specific fields
    is_featured = models.BooleanField(
        default=False,
        help_text=_("Show this bootcamp on homepage featured section")
    )
    total_duration_weeks = models.IntegerField(
        default=12,
        help_text=_("Total bootcamp duration in weeks")
    )
    skill_level = models.CharField(
        max_length=25,
        choices=LEVEL,
        default=BEGINNER,
        help_text=_("Recommended skill level for this bootcamp")
    )

    objects = ProgramManager()
    
    class Meta:
        verbose_name = _("Bootcamp Program")
        verbose_name_plural = _("Bootcamp Programs")
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"pk": self.pk})
    
    def get_course_count(self):
        """Return number of courses in this bootcamp"""
        return self.course_set.count()
    
    def get_video_count(self):
        """Return total number of videos across all courses"""
        from django.db.models import Count
        return UploadVideo.objects.filter(course__program=self).count()


@receiver(post_save, sender=Program)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=_(f"The program '{instance}' has been {verb}."))


@receiver(post_delete, sender=Program)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=_(f"The program '{instance}' has been deleted."))


class CourseManager(models.Manager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(code__icontains=query)
                | Q(slug__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset


class Course(models.Model):
    """
    Bootcamp Course Model
    Represents individual courses within a bootcamp program
    """
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(
        max_length=200, 
        null=True,
        help_text=_("Course title (e.g., 'Introduction to Machine Learning')")
    )
    code = models.CharField(
        max_length=200, 
        unique=True, 
        null=True,
        help_text=_("Unique course code (e.g., 'AI101')")
    )
    summary = models.TextField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text=_("Brief course description for participants")
    )
    program = models.ForeignKey(
        Program, 
        on_delete=models.CASCADE,
        verbose_name=_("Bootcamp Program"),
        help_text=_("The bootcamp program this course belongs to")
    )
    
    # Keep old fields for backward compatibility (will be deprecated)
    credit = models.IntegerField(null=True, default=0, blank=True)
    year = models.IntegerField(default=0, blank=True, null=True)
    semester = models.CharField(max_length=200, blank=True, null=True)
    is_elective = models.BooleanField(default=False, blank=True, null=True)
    
    # New bootcamp fields
    level = models.CharField(
        max_length=25, 
        choices=LEVEL, 
        null=True,
        blank=True,
        verbose_name=_("Experience Level"),
        help_text=_("Required experience level for participants")
    )
    module = models.CharField(
        choices=BOOTCAMP_MODULE, 
        max_length=200,
        default=MODULE_ONE,
        blank=True,
        null=True,
        verbose_name=_("Bootcamp Module"),
        help_text=_("Which module this course belongs to")
    )
    duration_weeks = models.IntegerField(
        choices=DURATION_CHOICES,
        default=8,
        blank=True,
        null=True,
        help_text=_("Bootcamp duration in weeks")
    )
    is_premium = models.BooleanField(
        default=False, 
        blank=True, 
        null=True,
        help_text=_("Is this a premium/paid course?")
    )

    objects = CourseManager()
    
    class Meta:
        verbose_name = _("Bootcamp Course")
        verbose_name_plural = _("Bootcamp Courses")
        ordering = ['title']

    def __str__(self):
        return "{0} ({1})".format(self.title, self.code)

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    @property
    def is_current_semester(self):
        """Backward compatibility property"""
        from core.models import Semester
        try:
            current_semester = Semester.objects.get(is_current_semester=True)
            if self.semester:
                return self.semester == current_semester.semester
            return True
        except:
            return True

    @property
    def is_current_module(self):
        """Check if course is in currently active module"""
        from core.models import Semester
        try:
            current_semester = Semester.objects.get(is_current_semester=True)
            # Map semester to module for backward compatibility
            semester_module_map = {
                'First': MODULE_ONE,
                'Second': MODULE_TWO,
                'Third': MODULE_THREE,
            }
            current_module = semester_module_map.get(current_semester.semester, MODULE_ONE)
            return self.module == current_module if self.module else True
        except:
            return True


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Course)


@receiver(post_save, sender=Course)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=_(f"The course '{instance}' has been {verb}."))


@receiver(post_delete, sender=Course)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=_(f"The course '{instance}' has been deleted."))


class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name=_("allocated_lecturer"),
    )
    courses = models.ManyToManyField(Course, related_name=_("allocated_course"))
    session = models.ForeignKey(
        "core.Session", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.lecturer.get_full_name

    def get_absolute_url(self):
        return reverse("edit_allocated_course", kwargs={"pk": self.pk})


class Upload(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="course_files/",
        help_text="Valid Files: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip",
        validators=[
            FileExtensionValidator(
                [
                    "pdf",
                    "docx",
                    "doc",
                    "xls",
                    "xlsx",
                    "ppt",
                    "pptx",
                    "zip",
                    "rar",
                    "7zip",
                ]
            )
        ],
    )
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext) - 1]

        if ext in ("doc", "docx"):
            return "word"
        elif ext == "pdf":
            return "pdf"
        elif ext in ("xls", "xlsx"):
            return "excel"
        elif ext in ("ppt", "pptx"):
            return "powerpoint"
        elif ext in ("zip", "rar", "7zip"):
            return "archive"

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


@receiver(post_save, sender=Upload)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=_(
                f"The file '{instance.title}' has been uploaded to the course '{instance.course}'."
            )
        )
    else:
        ActivityLog.objects.create(
            message=_(
                f"The file '{instance.title}' of the course '{instance.course}' has been updated."
            )
        )


@receiver(post_delete, sender=Upload)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=_(
            f"The file '{instance.title}' of the course '{instance.course}' has been deleted."
        )
    )


class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    # YouTube video integration
    youtube_url = models.URLField(
        max_length=500,
        help_text=_("YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)"),
        null=True,
        blank=True
    )
    
    # Keep file field for backward compatibility (optional)
    video = models.FileField(
        upload_to="course_videos/",
        help_text=_("Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3 (Optional if YouTube URL is provided)"),
        validators=[
            FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
        ],
        null=True,
        blank=True
    )
    
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    
    # Additional YouTube-specific fields
    video_duration = models.CharField(max_length=20, blank=True, help_text=_("Video duration (auto-populated)"))
    is_youtube_video = models.BooleanField(default=False, help_text=_("Automatically set if YouTube URL is provided"))

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse(
            "video_single", kwargs={"slug": self.course.slug, "video_slug": self.slug}
        )
    
    def get_youtube_embed_url(self):
        """Convert YouTube URL to embeddable format with security features"""
        if self.youtube_url and self.is_youtube_video:
            from .utils import extract_youtube_video_id
            video_id = extract_youtube_video_id(self.youtube_url)
            if video_id:
                # Use embed format with security parameters
                return f"https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&showinfo=0&fs=0&disablekb=1"
        return None
    
    def get_youtube_video_id(self):
        """Extract YouTube video ID from URL"""
        if self.youtube_url:
            from .utils import extract_youtube_video_id
            return extract_youtube_video_id(self.youtube_url)
        return None
    
    def clean(self):
        """Validate that either YouTube URL or video file is provided"""
        from django.core.exceptions import ValidationError
        if not self.youtube_url and not self.video:
            raise ValidationError(_("Either YouTube URL or video file must be provided"))
    
    def save(self, *args, **kwargs):
        # Auto-detect if this is a YouTube video
        if self.youtube_url:
            self.is_youtube_video = True
        else:
            self.is_youtube_video = False
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Only delete file if it exists (YouTube videos don't have files)
        if self.video:
            self.video.delete()
        super().delete(*args, **kwargs)


def video_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(video_pre_save_receiver, sender=UploadVideo)


@receiver(post_save, sender=UploadVideo)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=_(
                f"The video '{instance.title}' has been uploaded to the course {instance.course}."
            )
        )
    else:
        ActivityLog.objects.create(
            message=_(
                f"The video '{instance.title}' of the course '{instance.course}' has been updated."
            )
        )


@receiver(post_delete, sender=UploadVideo)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=_(
            f"The video '{instance.title}' of the course '{instance.course}' has been deleted."
        )
    )


class CourseOffer(models.Model):
    _("""NOTE: Only department head can offer semester courses""")

    dep_head = models.ForeignKey("accounts.DepartmentHead", on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.dep_head)


class VideoProgress(models.Model):
    """Track student progress for video lectures"""
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}
    )
    video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE)
    
    # Progress tracking fields
    watch_time = models.PositiveIntegerField(default=0, help_text=_("Watch time in seconds"))
    total_duration = models.PositiveIntegerField(default=0, help_text=_("Total video duration in seconds"))
    last_position = models.PositiveIntegerField(default=0, help_text=_("Last watched position in seconds"))
    
    # Status fields
    is_completed = models.BooleanField(default=False)
    completion_percentage = models.FloatField(default=0.0, help_text=_("Completion percentage (0-100)"))
    
    # Timestamps
    first_watched = models.DateTimeField(auto_now_add=True)
    last_watched = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'video')
        ordering = ['-last_watched']
    
    def __str__(self):
        return f"{self.student.username} - {self.video.title} ({self.completion_percentage:.1f}%)"
    
    def save(self, *args, **kwargs):
        # Calculate completion percentage
        if self.total_duration > 0:
            self.completion_percentage = min((self.watch_time / self.total_duration) * 100, 100.0)
        
        # Mark as completed if watch time is >= 90% of total duration
        if self.completion_percentage >= 90.0 and not self.is_completed:
            self.is_completed = True
            if not self.completed_at:
                from django.utils import timezone
                self.completed_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def progress_display(self):
        """Human readable progress display"""
        return f"{self.completion_percentage:.1f}%"
    
    @property
    def time_watched_display(self):
        """Convert seconds to human readable format"""
        hours = self.watch_time // 3600
        minutes = (self.watch_time % 3600) // 60
        seconds = self.watch_time % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"


@receiver(post_save, sender=VideoProgress)
def log_video_progress(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=_(f"Student '{instance.student.username}' started watching '{instance.video.title}'.")
        )
    elif instance.is_completed and instance.completion_percentage >= 90:
        ActivityLog.objects.create(
            message=_(f"Student '{instance.student.username}' completed watching '{instance.video.title}'.")
        )
