from typing import Tuple

height_reference = 1_440
width_reference = 2_560


def resize_template(
    width_orig: int,
    height_orig: int,
    width_orig_template: int,
    height_orig_template: int,
) -> Tuple[int, int]:


    width_resize, height_resize = resize_origin_image_size(width_orig, height_orig)

    

    return 0, 0


def resize_origin_image_size(
        width_orig: int,
        height_orig: int,
):
    height_resize = height_reference
    width_resize = int((width_orig / height_orig) * height_resize)

    return width_resize, height_resize