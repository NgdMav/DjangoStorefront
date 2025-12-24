from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 1024

    if file.size > max_size_kb * 1024:
        raise ValidationError(f"File size is too big(file must be <= {max_size_kb} KB)")