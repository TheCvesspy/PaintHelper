"""
Image validation and optimization module for secure uploads.

Provides multi-layer security validation and automatic image optimization
to ensure uploaded images are safe and fit within storage constraints.
"""
import os
from PIL import Image
import io

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DIMENSIONS = (2048, 2048)  # Target max dimensions (will resize to fit)
MIN_QUALITY = 60  # Minimum JPEG quality before giving up

class ImageValidationError(Exception):
    """Custom exception for image validation failures"""
    pass

def validate_and_optimize_image(file_data: bytes, filename: str) -> dict:
    """
    Validates and automatically optimizes images to fit requirements.
    
    Instead of rejecting large images, this function:
    1. Validates the image is safe (correct format, no exploits)
    2. Resizes if dimensions exceed MAX_DIMENSIONS
    3. Compresses if file size exceeds MAX_FILE_SIZE
    4. Strips EXIF data for security
    
    Args:
        file_data: Raw file bytes
        filename: Original filename (for extension check)
    
    Returns:
        dict with validation results and optimized image data:
        {
            'valid': bool,
            'format': str,  # 'jpeg', 'png', or 'webp'
            'cleaned_data': bytes,  # Optimized image bytes
            'original_size': tuple,  # (width, height)
            'final_size': tuple,  # (width, height) after resize
            'file_size': int,  # Final file size in bytes
            'was_resized': bool,
            'was_compressed': bool,
            'final_quality': int  # JPEG quality used
        }
    
    Raises:
        ImageValidationError: If image cannot be validated or optimized
    """
    if len(file_data) == 0:
        raise ImageValidationError("Empty file")
    
    # 1. Check file extension (allowlist)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ImageValidationError(
            f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 2. Verify actual image format by opening with PIL
    # This replaces imghdr (removed in Python 3.13)
    try:
        with Image.open(io.BytesIO(file_data)) as test_img:
            img_format = test_img.format
            if img_format is None or img_format.lower() not in ['jpeg', 'png', 'webp']:
                raise ImageValidationError("File is not a valid image format (JPEG/PNG/WEBP)")
            img_format = img_format.lower()
    except Exception as e:
        raise ImageValidationError(f"Invalid image file: {str(e)}")
    
    # 3. Open and validate with PIL
    try:
        with Image.open(io.BytesIO(file_data)) as img:
            original_size = img.size
            was_resized = False
            was_compressed = False
            
            # Convert RGBA to RGB if saving as JPEG
            if img.mode in ('RGBA', 'LA', 'P') and img_format == 'jpeg':
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB' and img_format == 'jpeg':
                img = img.convert('RGB')
            
            # 4. Resize if dimensions exceed maximum
            if img.size[0] > MAX_DIMENSIONS[0] or img.size[1] > MAX_DIMENSIONS[1]:
                img.thumbnail(MAX_DIMENSIONS, Image.Resampling.LANCZOS)
                was_resized = True
            
            # 5. Strip EXIF data and optimize size
            save_format = 'JPEG' if img_format == 'jpeg' else img_format.upper()
            quality = 85  # Start with good quality
            
            # Try to compress to under MAX_FILE_SIZE
            for attempt in range(5):  # Max 5 compression attempts
                output = io.BytesIO()
                
                if save_format == 'JPEG':
                    img.save(output, format=save_format, quality=quality, optimize=True)
                elif save_format == 'PNG':
                    img.save(output, format=save_format, optimize=True)
                elif save_format == 'WEBP':
                    img.save(output, format=save_format, quality=quality, method=6)
                
                clean_data = output.getvalue()
                
                # Check if we're under the limit
                if len(clean_data) <= MAX_FILE_SIZE:
                    if attempt > 0:
                        was_compressed = True
                    break
                
                # If still too large, reduce quality or convert format
                if save_format in ['JPEG', 'WEBP']:
                    quality = max(MIN_QUALITY, quality - 10)
                    if quality == MIN_QUALITY and attempt == 4:
                        raise ImageValidationError(
                            f"Could not compress image to under {MAX_FILE_SIZE/1024/1024}MB. "
                            f"Current size: {len(clean_data)/1024/1024:.2f}MB. "
                            f"Try reducing image dimensions before uploading."
                        )
                elif save_format == 'PNG':
                    # PNG compression is limited, convert to JPEG instead
                    save_format = 'JPEG'
                    img = img.convert('RGB')
                    quality = 85
                    was_compressed = True
            
            # Prepare result with metadata
            result = {
                'valid': True,
                'format': 'jpeg' if save_format == 'JPEG' else img_format,
                'cleaned_data': clean_data,
                'original_size': original_size,
                'final_size': img.size,
                'file_size': len(clean_data),
                'was_resized': was_resized,
                'was_compressed': was_compressed,
                'final_quality': quality if save_format in ['JPEG', 'WEBP'] else 100
            }
            
            return result
    
    except ImageValidationError:
        raise
    except Exception as e:
        raise ImageValidationError(f"Invalid image file: {str(e)}")

def get_safe_mime_type(img_format: str) -> str:
    """Maps image format to MIME type"""
    mapping = {
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
    }
    return mapping.get(img_format, 'application/octet-stream')
