import cv2
import numpy as np
from src.utils.logger import logger

class VisionEngine:
    def __init__(self, templates_dir="images"):
        self.templates_dir = templates_dir
        self.templates = {}

    def load_template(self, name, filename):
        """Loads an image template from disk."""
        path = f"{self.templates_dir}/{filename}"
        template = cv2.imread(path, cv2.IMREAD_COLOR)
        if template is None:
            logger.error(f"Failed to load template: {path}")
            return False
        self.templates[name] = template
        logger.debug(f"Loaded template '{name}' from {path}")
        return True

    def find_template(self, screen_image, template_name, threshold=0.8):
        """
        Searches for a template within the screen_image.
        screen_image: A PIL Image or numpy array (BGR).
        Returns a tuple (x, y) of the center point if found, else None.
        """
        if template_name not in self.templates:
            logger.error(f"Template '{template_name}' not loaded.")
            return None

        # Convert PIL Image to cv2 format (BGR) if necessary
        if not isinstance(screen_image, np.ndarray):
            screen_np = np.array(screen_image)
            # PIL is RGB, cv2 is BGR
            if len(screen_np.shape) == 3 and screen_np.shape[2] == 3:
                screen_cv = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            elif len(screen_np.shape) == 3 and screen_np.shape[2] == 4:
                screen_cv = cv2.cvtColor(screen_np, cv2.COLOR_RGBA2BGR)
            else:
                screen_cv = screen_np
        else:
            screen_cv = screen_image

        template = self.templates[template_name]

        # Ensure dimensions match for matching (screen must be larger or equal to template)
        if screen_cv.shape[0] < template.shape[0] or screen_cv.shape[1] < template.shape[1]:
            logger.warning("Screen image is smaller than template.")
            return None

        # Perform template matching
        res = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            # Calculate center of the matched region
            h, w = template.shape[:-1] if len(template.shape) == 3 else template.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)

        return None
