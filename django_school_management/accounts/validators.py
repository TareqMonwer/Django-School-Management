import imghdr
import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
MAX_UPLOAD_SIZE = getattr(settings, 'MAX_PROFILE_PICTURE_SIZE', 5 * 1024 * 1024)  # 5 MB default


def validate_profile_image(image):
    """Validate uploaded file is a real image with safe type and size."""
    if image.size > MAX_UPLOAD_SIZE:
        raise ValidationError(f'File size must be under {filesizeformat(MAX_UPLOAD_SIZE)}.')

    ext = os.path.splitext(image.name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(f'Invalid file extension. Allowed: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}.')

    content_type = getattr(image, 'content_type', '')
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(f'Invalid file type. Only {", ".join(ALLOWED_IMAGE_TYPES)} images are allowed.')

    header = image.read(32)
    image.seek(0)

    detected = imghdr.what(image, h=header)
    image.seek(0)
    if detected not in ('jpeg', 'png', 'gif', 'webp'):
        raise ValidationError('File content does not match a valid image format.')


def upload_profile_image(user, image):
    """Validate and save a profile image. Returns the image URL."""
    validate_profile_image(image)
    user.profile.profile_picture = image
    user.profile.save()
    return user.profile.profile_picture.url
