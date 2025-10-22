from django import forms
from accounts.models import User
from .models import Program, Course, CourseAllocation, Upload, UploadVideo


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})


class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["code"].widget.attrs.update({"class": "form-control"})
        # self.fields['courseUnit'].widget.attrs.update({'class': 'form-control'})
        self.fields["credit"].widget.attrs.update({"class": "form-control"})
        self.fields["summary"].widget.attrs.update({"class": "form-control"})
        self.fields["program"].widget.attrs.update({"class": "form-control"})
        self.fields["level"].widget.attrs.update({"class": "form-control"})
        self.fields["year"].widget.attrs.update({"class": "form-control"})
        self.fields["semester"].widget.attrs.update({"class": "form-control"})


class CourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by("level"),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "browser-default checkbox"}
        ),
        required=True,
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={"class": "browser-default custom-select"}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ["lecturer", "courses"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(CourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields["lecturer"].queryset = User.objects.filter(is_lecturer=True)


class EditCourseAllocationForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by("level"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={"class": "browser-default custom-select"}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ["lecturer", "courses"]

    def __init__(self, *args, **kwargs):
        #    user = kwargs.pop('user')
        super(EditCourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields["lecturer"].queryset = User.objects.filter(is_lecturer=True)


# Upload files to specific course
class UploadFormFile(forms.ModelForm):
    class Meta:
        model = Upload
        fields = (
            "title",
            "file",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["file"].widget.attrs.update({"class": "form-control"})


# Upload video to specific course
class UploadFormVideo(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = (
            "title",
            "youtube_url",
            "video",
            "summary",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter video title"
        })
        
        self.fields["youtube_url"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "https://www.youtube.com/watch?v=VIDEO_ID (Recommended for storage optimization)"
        })
        
        self.fields["video"].widget.attrs.update({
            "class": "form-control",
            "accept": "video/*"
        })
        
        self.fields["summary"].widget.attrs.update({
            "class": "form-control",
            "rows": 3,
            "placeholder": "Enter video description (optional)"
        })
        
        # Add help text
        self.fields["youtube_url"].help_text = "Paste YouTube video URL here. This is recommended as it saves server storage space."
        self.fields["video"].help_text = "Upload video file only if YouTube URL is not available. Large files may cause storage issues."

    def clean(self):
        cleaned_data = super().clean()
        youtube_url = cleaned_data.get('youtube_url')
        video = cleaned_data.get('video')
        
        # Validate that at least one video source is provided
        if not youtube_url and not video:
            raise forms.ValidationError("Please provide either a YouTube URL or upload a video file.")
        
        # Validate YouTube URL if provided
        if youtube_url:
            from .utils import validate_youtube_url
            is_valid, video_id, error_msg = validate_youtube_url(youtube_url)
            if not is_valid:
                raise forms.ValidationError(f"Invalid YouTube URL: {error_msg}")
        
        return cleaned_data
