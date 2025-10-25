from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserChangeForm,
    UserCreationForm,
)
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from course.models import Program

from .models import GENDERS, LEVEL, RELATION_SHIP, Parent, Student, User


class StaffAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Username",
        required=False,
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First Name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last Name",
    )

    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Mobile No.",
    )

    email = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Email",
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password",
        required=False,
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password Confirmation",
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.phone = self.cleaned_data.get("phone")
        user.address = self.cleaned_data.get("address")
        user.email = self.cleaned_data.get("email")

        # Mark as form registration to prevent signal from overwriting password
        user._form_registration = True

        if commit:
            user.save()

        return user


class StudentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"type": "text", "class": "form-control", "id": "username_id"}
        ),
        label="Username",
        required=False,
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last name",
    )

    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    level = forms.CharField(
        widget=forms.Select(
            choices=LEVEL,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Program",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password",
        required=False,
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password Confirmation",
        required=False,
    )

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.gender = self.cleaned_data.get("gender")
        user.address = self.cleaned_data.get("address")
        user.phone = self.cleaned_data.get("phone")
        user.address = self.cleaned_data.get("address")
        user.email = self.cleaned_data.get("email")

        # Mark as form registration to prevent signal from overwriting password
        user._form_registration = True

        if commit:
            user.save()
            Student.objects.create(
                student=user,
                level=self.cleaned_data.get("level"),
                program=self.cleaned_data.get("program"),
            )

        return user


class ProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First Name",
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last Name",
    )

    gender = forms.CharField(
        widget=forms.Select(
            choices=GENDERS,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Phone No.",
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address / city",
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "phone",
            "address",
            "picture",
        ]


class ProgramUpdateForm(UserChangeForm):
    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Program",
    )

    class Meta:
        model = Student
        fields = ["program"]


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-mail address. "
            self.add_error("email", msg)
            return email


class ParentAddForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Username",
    )
    address = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Address",
    )

    phone = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Mobile No.",
    )

    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="First name",
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
            }
        ),
        label="Last name",
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(
            attrs={"class": "browser-default custom-select form-control"}
        ),
        label="Student",
    )

    relation_ship = forms.CharField(
        widget=forms.Select(
            choices=RELATION_SHIP,
            attrs={
                "class": "browser-default custom-select form-control",
            },
        ),
    )

    password1 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password",
    )

    password2 = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control",
            }
        ),
        label="Password Confirmation",
    )

    # def validate_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email__iexact=email, is_active=True).exists():
    #         raise forms.ValidationError("Email has taken, try another email address. ")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_parent = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.address = self.cleaned_data.get("address")
        user.phone = self.cleaned_data.get("phone")
        user.email = self.cleaned_data.get("email")

        # Mark as form registration to prevent signal from overwriting password
        user._form_registration = True

        user.save()
        parent = Parent.objects.create(
            user=user,
            student=self.cleaned_data.get("student"),
            relation_ship=self.cleaned_data.get("relation_ship"),
        )
        parent.save()
        return user


class StudentLoginForm(AuthenticationForm):
    """Enhanced login form for bootcamp/masterclass participants - supports email OR phone login"""

    username = forms.CharField(
        label=_("Email or Phone Number"),
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": " ",
                "id": "student_username",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": " ",
                "id": "student_password",
                "autocomplete": "current-password",
            }
        ),
    )

    remember_me = forms.BooleanField(
        label=_("Remember me"),
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "id": "remember_me",
            }
        ),
    )

    def clean(self):
        username_or_phone = self.cleaned_data.get("username")  # Can be email OR phone
        password = self.cleaned_data.get("password")

        if username_or_phone is not None and password:
            user = None

            try:
                # Try to find user by email OR phone number
                # Check if it looks like a phone number (contains only digits, spaces, +, -, ())
                import re

                if re.match(r"^[\d\s\+\-\(\)]+$", username_or_phone):
                    # Looks like phone number - clean it (remove spaces, dashes, etc.)
                    cleaned_phone = re.sub(r"[\s\-\(\)]", "", username_or_phone)

                    # Search by phone (exact match or without country code)
                    user = User.objects.filter(
                        Q(phone__iexact=username_or_phone)
                        | Q(phone__iexact=cleaned_phone)
                        | Q(phone__endswith=cleaned_phone[-10:])  # Last 10 digits
                    ).first()

                    if not user:
                        raise forms.ValidationError(
                            _(
                                "No account found with this phone number. Please check and try again."
                            ),
                            code="phone_not_found",
                        )
                else:
                    # Looks like email - case-insensitive search
                    user = User.objects.filter(email__iexact=username_or_phone).first()

                    if not user:
                        raise forms.ValidationError(
                            _(
                                "No account found with this email. Please register first or check your email address."
                            ),
                            code="email_not_found",
                        )

                # Check if user is a student
                if not user.is_student:
                    raise forms.ValidationError(
                        _(
                            "This login is only for bootcamp participants. Please use the correct login page."
                        ),
                        code="not_student",
                    )

                # Check if user is active
                if not user.is_active:
                    raise forms.ValidationError(
                        _("Your account is inactive. Please contact support."),
                        code="inactive_account",
                    )

                # Ensure Student profile exists
                if not Student.objects.filter(student=user).exists():
                    # Auto-create Student profile if missing
                    from course.models import Program

                    default_program = Program.objects.first()
                    if default_program:
                        Student.objects.create(
                            student=user, level="Beginner", program=default_program
                        )

                # Authenticate using the actual username (not email/phone!)
                self.user_cache = authenticate(
                    self.request,
                    username=user.username,  # Use the actual username from database
                    password=password,
                )

                if self.user_cache is None:
                    raise forms.ValidationError(
                        _(
                            "Invalid password. Please check your password and try again."
                        ),
                        code="invalid_password",
                    )
                else:
                    self.confirm_login_allowed(self.user_cache)

            except forms.ValidationError:
                # Re-raise validation errors (these are our custom errors)
                raise
            except User.DoesNotExist:
                # User not found (shouldn't happen as we check with .first())
                raise forms.ValidationError(
                    _("Account not found. Please check your credentials."),
                    code="user_not_found",
                )
            except Exception as e:
                # Log the actual error for debugging
                import logging

                logger = logging.getLogger(__name__)
                logger.error(f"Login error for {username_or_phone}: {str(e)}")

                # Show user-friendly error with hint about the actual problem
                raise forms.ValidationError(
                    _("Login failed. Error: %(error)s") % {"error": str(e)},
                    code="login_error",
                )

        return self.cleaned_data


class StudentRegistrationForm(UserCreationForm):
    """Registration form for Bootcamp/Masterclass participants"""

    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": _("Enter your first name"),
                "required": "required",
            }
        ),
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": _("Enter your last name"),
                "required": "required",
            }
        ),
    )

    email = forms.EmailField(
        label=_("Email Address"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your email address"),
                "required": "required",
            }
        ),
    )

    phone = forms.CharField(
        label=_("Phone Number"),
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control",
                "placeholder": _("Enter your WhatsApp or contact number"),
                "required": "required",
            }
        ),
    )

    city = forms.CharField(
        label=_("City"),
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter your city"),
                "required": "required",
            }
        ),
    )

    level = forms.ChoiceField(
        label=_("Experience Level"),
        choices=LEVEL,
        required=True,
        widget=forms.Select(attrs={"class": "form-control", "required": "required"}),
        help_text=_("Select your current experience level with technology"),
    )

    program = forms.ModelChoiceField(
        label=_("Bootcamp/Masterclass"),
        queryset=Program.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control", "required": "required"}),
        help_text=_("Select the bootcamp or masterclass you want to join"),
    )

    password1 = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter a strong password"),
                "required": "required",
            }
        ),
        help_text=_("Password must be at least 8 characters long"),
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Confirm your password"),
                "required": "required",
            }
        ),
    )

    terms_accepted = forms.BooleanField(
        label=_("I agree to the terms and conditions"),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "level",
            "program",
            "password1",
            "password2",
            "terms_accepted",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email address is already registered."))
        return email

    @transaction.atomic
    def save(self, commit=True):
        # Create user object without saving to database yet
        user = User()

        # Set additional student-specific fields
        user.is_student = True
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.phone = self.cleaned_data.get("phone")
        user.address = self.cleaned_data.get("city")  # Using address field for city

        # Generate unique username from email
        email_username = self.cleaned_data.get("email").split("@")[0]
        base_username = f"user_{email_username}"
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        user.username = username

        # Hash and set password properly using set_password
        user.set_password(self.cleaned_data.get("password1"))

        # Mark as form registration to prevent signal from overwriting password
        user._form_registration = True

        if commit:
            # Save the user with hashed password
            user.save()

            # Create Student profile
            student = Student.objects.create(
                student=user,
                level=self.cleaned_data.get("level"),
                program=self.cleaned_data.get("program"),
            )
            student.save()

        return user
