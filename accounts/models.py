from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from course.models import Program

from .validators import ASCIIUsernameValidator

# Experience Levels for Bootcamp/Masterclass participants
BEGINNER = _("Beginner")
INTERMEDIATE = _("Intermediate")
ADVANCED = _("Advanced")
EXPERT = _("Expert")

LEVEL = (
    (BEGINNER, _("Beginner - New to the technology")),
    (INTERMEDIATE, _("Intermediate - Some experience")),
    (ADVANCED, _("Advanced - Strong knowledge")),
    (EXPERT, _("Expert - Industry professional")),
)

FATHER = _("Father")
MOTHER = _("Mother")
BROTHER = _("Brother")
SISTER = _("Sister")
GRAND_MOTHER = _("Grand mother")
GRAND_FATHER = _("Grand father")
OTHER = _("Other")

RELATION_SHIP = (
    (FATHER, _("Father")),
    (MOTHER, _("Mother")),
    (BROTHER, _("Brother")),
    (SISTER, _("Sister")),
    (GRAND_MOTHER, _("Grand mother")),
    (GRAND_FATHER, _("Grand father")),
    (OTHER, _("Other")),
)


class CustomUserManager(UserManager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset

    def get_student_count(self):
        return self.model.objects.filter(is_student=True).count()

    def get_lecturer_count(self):
        return self.model.objects.filter(is_lecturer=True).count()

    def get_superuser_count(self):
        return self.model.objects.filter(is_superuser=True).count()

    def make_random_password(
        self,
        length=10,
        allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789",
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        import random

        return "".join(random.choice(allowed_chars) for i in range(length))


GENDERS = ((_("M"), _("Male")), (_("F"), _("Female")))


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_dep_head = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    picture = models.ImageField(
        upload_to="profile_pictures/%y/%m/%d/", default="default.png", null=True
    )
    # Keep a single email field. Make it nullable for existing rows so
    # migrations can run non-interactively on deployments where the DB
    # may already contain NULL emails. The unique constraint is preserved.
    email = models.EmailField(
        _("email address"),
        unique=True,
        null=True,
        blank=True,
        help_text=_("Required. Used for login and notifications."),
    )

    username_validator = ASCIIUsernameValidator()

    objects = CustomUserManager()

    class Meta:
        ordering = ("-date_joined",)

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return "{} ({})".format(self.username, self.get_full_name)

    @property
    def get_user_role(self):
        if self.is_superuser:
            role = _("Admin")
        elif self.is_student:
            role = _("Student")
        elif self.is_lecturer:
            role = _("Lecturer")
        elif self.is_parent:
            role = _("Parent")

        return role

    def get_picture(self):
        """Return a safe URL for the user's avatar.
        Prefer the uploaded picture if it exists; otherwise return a static fallback
        that is always available in collected static files.
        """
        static_fallback = settings.STATIC_URL + "img/savvyindians-logo.png"
        try:
            # If picture is not set or the file is missing, return static fallback
            if not self.picture or not self.picture.name:
                return static_fallback
            if not self.picture.storage.exists(self.picture.name):
                return static_fallback
            # Use the uploaded picture URL
            return self.picture.url
        except Exception:
            # Return static fallback on any error (missing file, storage issues, etc.)
            return static_fallback

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        # Store the old picture path before saving
        old_picture = None
        if self.pk:
            old_picture = User.objects.get(pk=self.pk).picture

        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except Exception:
            # Ignore image processing errors safely
            pass

        # Delete the old picture if it has changed and is not the default
        if old_picture and self.picture and old_picture.url != self.picture.url:
            if old_picture.url != settings.MEDIA_URL + "default.png":
                old_picture.delete(save=False)

    def delete(self, *args, **kwargs):
        try:
            if self.picture and getattr(self.picture, 'url', None) != settings.MEDIA_URL + "default.png":
                self.picture.delete()
        except Exception:
            # If picture deletion fails, continue with user deletion
            pass
        super().delete(*args, **kwargs)


class StudentManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = Q(level__icontains=query) | Q(program__icontains=query)
            qs = qs.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Student(models.Model):
    """
    Bootcamp/Masterclass Participant Model
    Stores information about learners enrolled in AI bootcamps and masterclasses
    """

    # Link to the User model (keep a single OneToOneField)
    student = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    level = models.CharField(
        max_length=25,
        choices=LEVEL,
        null=True,
        verbose_name=_("Experience Level"),
        help_text=_("Your current experience level with technology"),
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_("Bootcamp/Masterclass"),
        help_text=_("Select the bootcamp or masterclass you want to join"),
    )

    objects = StudentManager()

    class Meta:
        ordering = ("-student__date_joined",)
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")

    def __str__(self):
        return self.student.get_full_name

    @classmethod
    def get_gender_count(cls):
        males_count = Student.objects.filter(student__gender="M").count()
        females_count = Student.objects.filter(student__gender="F").count()

        return {"M": males_count, "F": females_count}

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    def delete(self, force=False, *args, **kwargs):
        """
        Delete student profile.
        - If force=True: only delete the Student instance (used when the User is being deleted).
        - If force=False: delete the Student and then delete the associated User to avoid orphaned accounts.
        """
        if force:
            super().delete(*args, **kwargs)
            return

        # Normal deletion - delete Student then associated User
        user = self.student
        super().delete(*args, **kwargs)
        try:
            if user:
                user.delete()
        except Exception:
            # If user deletion fails for any reason, ignore to avoid leaving the DB in an inconsistent state
            pass


class Parent(models.Model):
    """
    Connect student with their parent, parents can
    only view their connected students information
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # What is the relationship between the student and
    # the parent (i.e. father, mother, brother, sister)
    relation_ship = models.TextField(choices=RELATION_SHIP, blank=True)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return self.user.username


class DepartmentHead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ("-user__date_joined",)

    def __str__(self):
        return "{}".format(self.user)
