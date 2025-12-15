from PIL import Image, ImageOps
from io import BytesIO

def process_image_from_path(path, *, rotate=0, width=None, height=None, thumb=False, crop_box=None, fmt='JPEG'):
    """Open image at path, apply simple operations and return bytes and mime type.

    Args:
        path: filesystem path to image
        rotate: degrees to rotate (clockwise)
        width: target width (keeps aspect ratio if height None)
        height: target height
        thumb: create a thumbnail (uses width/height)
        crop_box: tuple (left, upper, right, lower)
        fmt: output format (JPEG/PNG)

    Returns:
        bytes, mime_type
    """
    im = Image.open(path)
    # Convert to RGBA for consistent processing when needed
    mode = im.mode
    if rotate:
        im = im.rotate(-rotate, expand=True)
    if crop_box:
        im = im.crop(crop_box)
    if width or height:
        w = width
        h = height
        if thumb:
            size = (width or 128, height or 128)
            im.thumbnail(size, Image.LANCZOS)
        else:
            # Preserve aspect ratio if only one provided
            if w and not h:
                ratio = w / float(im.width)
                h = int(im.height * ratio)
            elif h and not w:
                ratio = h / float(im.height)
                w = int(im.width * ratio)
            if w and h:
                im = im.resize((int(w), int(h)), Image.LANCZOS)

    # Auto-orient and contrast
    try:
        im = ImageOps.exif_transpose(im)
    except Exception:
        pass

    bio = BytesIO()
    out_fmt = fmt.upper()
    if out_fmt == 'JPEG' and im.mode in ('RGBA', 'LA'):
        # JPEG doesn't support alpha; flatten on white
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        bg.save(bio, format='JPEG', quality=85)
        mime = 'image/jpeg'
    else:
        im.save(bio, format=out_fmt)
        mime = f'image/{out_fmt.lower()}'

    bio.seek(0)
    return bio.read(), mime
