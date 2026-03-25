from django import forms

from content.models import GalleryImage, PageSection


class PageSectionForm(forms.ModelForm):
    class Meta:
        model = PageSection
        fields = ["heading", "body", "image", "display_order", "is_active"]


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["title", "caption", "category", "image", "display_order", "is_active"]

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image must be 5MB or smaller.")
        return image
