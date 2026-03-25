from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from dashboard.forms import GalleryImageForm


def _large_image_upload():
    # BMP is uncompressed, so this reliably exceeds 5MB.
    image = Image.new("RGB", (2000, 2000), color=(10, 20, 30))
    buffer = BytesIO()
    image.save(buffer, format="BMP")
    return SimpleUploadedFile(
        "large.bmp",
        buffer.getvalue(),
        content_type="image/bmp",
    )


class GalleryImageFormValidationTests(SimpleTestCase):
    def test_rejects_images_larger_than_5mb(self):
        form = GalleryImageForm(
            data={
                "title": "Large Image",
                "display_order": 1,
                "is_active": True,
            },
            files={"image": _large_image_upload()},
        )
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
        self.assertIn("5MB", str(form.errors["image"]))
