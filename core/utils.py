from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages


def send_email(user, subject, msg):
    send_mail(
        subject,
        msg,
        settings.EMAIL_FROM_ADDRESS,
        [user.email],
        fail_silently=False,
    )


def send_html_email(subject, recipient_list, template, context):
    """A function responsible for sending HTML email"""
    # Render the HTML template
    html_message = render_to_string(template, context)

    # Generate plain text version of the email (optional)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_FROM_ADDRESS,
        recipient_list,
        html_message=html_message,
    )


# Common utilities to reduce code duplication across the project
def handle_form_submission(request, form_class, template_name, success_url, 
                         success_message, error_message=None, context=None, instance=None):
    """
    Generic function to handle form submission (add/edit operations).
    
    Args:
        request: HTTP request object
        form_class: Django form class
        template_name: Template to render
        success_url: URL to redirect on success
        success_message: Success message template (can use {title} placeholder)
        error_message: Error message (default: "Please correct the error(s) below.")
        context: Additional context dictionary
        instance: Instance for edit operations
    """
    if error_message is None:
        error_message = "Please correct the error(s) below."
    
    if context is None:
        context = {}
    
    if request.method == "POST":
        if instance:
            form = form_class(request.POST, request.FILES, instance=instance)
        else:
            form = form_class(request.POST, request.FILES)
            
        if form.is_valid():
            saved_instance = form.save()
            # Handle success message formatting
            if hasattr(saved_instance, 'title') and '{title}' in success_message:
                message = success_message.format(title=saved_instance.title)
            else:
                message = success_message
            messages.success(request, message)
            return redirect(success_url)
        else:
            messages.error(request, error_message)
    else:
        if instance:
            form = form_class(instance=instance)
        else:
            form = form_class()
    
    context.update({"form": form})
    return render(request, template_name, context)


def handle_delete_operation(request, model_class, pk_field, redirect_url, 
                          success_message, validation_func=None):
    """
    Generic function to handle delete operations.
    
    Args:
        request: HTTP request object
        model_class: Django model class
        pk_field: Primary key value or dict with lookup fields
        redirect_url: URL to redirect after deletion
        success_message: Success message template (can use {title} placeholder)
        validation_func: Optional function to validate if deletion is allowed
    """
    if isinstance(pk_field, dict):
        instance = model_class.objects.get(**pk_field)
    else:
        instance = model_class.objects.get(pk=pk_field)
    
    # Check if deletion is allowed
    if validation_func and not validation_func(instance):
        return redirect(redirect_url)
    
    # Store title before deletion
    title = getattr(instance, 'title', str(instance))
    instance.delete()
    
    # Format success message
    if '{title}' in success_message:
        message = success_message.format(title=title)
    else:
        message = success_message
    
    messages.success(request, message)
    return redirect(redirect_url)


# Common validation functions
def validate_current_session_deletion(session):
    """Validate if current session can be deleted."""
    if session.is_current_session:
        messages.error(None, "You cannot delete current session")
        return False
    return True


def validate_current_semester_deletion(semester):
    """Validate if current semester can be deleted."""
    if semester.is_current_semester:
        messages.error(None, "You cannot delete current semester")
        return False
    return True


# Common context data
def get_pagination_context(queryset, request, per_page=10):
    """Get paginated context for list views."""
    from django.core.paginator import Paginator
    
    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page")
    return paginator.get_page(page)


def add_standard_context(context, title=None, **kwargs):
    """Add standard context variables."""
    if title:
        context["title"] = title
    context.update(kwargs)
    return context
