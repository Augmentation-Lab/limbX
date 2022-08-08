"""
1. Segment image into object regions.
2. Crop image to only include eye-tracked object without bg.
3. Use SIFT to map features from cropped image to target image.
4. Segment target image into object regions.
5. Select the object region containing the most mapped points.
"""

def process_input_img(img):
    """
    Segment image into object regions.
    """
    