from django import forms

from content.models import GalleryImage, PageSection


class PageSectionForm(forms.ModelForm):
    class Meta:
        model = PageSection
        fields = ["heading", "body", "image", "display_order", "is_active"]


class GalleryImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        allow_multiple_upload = kwargs.pop("allow_multiple_upload", False)
        super().__init__(*args, **kwargs)
        if allow_multiple_upload:
            self.fields["image"].widget.attrs["multiple"] = True

    class Meta:
        model = GalleryImage
        fields = ["title", "caption", "category", "image", "display_order", "is_active"]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image must be 5MB or smaller.")
        return image
