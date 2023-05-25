import cv2
import numpy as np
from constants.constants import TEMP_DIR


class LeafDetector():
    def __init__(self) -> None:
        pass

    def detect(self, filename):
        response = {}
        file_path = str(TEMP_DIR / filename)
        try:
            image = cv2.imread(file_path)
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur to reduce noise
            blur = cv2.GaussianBlur(gray, (3, 3), 0)

            # Perform adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 37, 5)

            # Find contours in the thresholded image
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Find the contour with the largest area
            max_contour = max(contours, key=cv2.contourArea)

            # Find the bounding box around the largest contour
            x, y, w, h = cv2.boundingRect(max_contour)

            # Adjust the bounding box dimensions
            padding = -27  # Increase this value to move the bounding box closer to the leaf edges
            x -= padding
            y -= padding
            w += 2 * padding
            h += 2 * padding

            # Draw the adjusted bounding box on the original image
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculate the length and width of the leaf with respect to the page dimensions
            page_height_cm = 14.5
            page_width_cm = 10.5

            leaf_length_cm = (h / image.shape[0]) * page_height_cm
            leaf_width_cm = (w / image.shape[1]) * page_width_cm

            # Store the length and width in variables
            length = leaf_length_cm
            width = leaf_width_cm

            # Draw the length and width text on the image
            text = "Length: {:.2f} cm".format(leaf_length_cm)
            cv2.putText(image, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            text = "Width: {:.2f} cm".format(leaf_width_cm)
            cv2.putText(image, text, (x, y + h + 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Resize the image
            resized_image = cv2.resize(image, None, fx=0.5, fy=0.5)

            # Storing response in response dictionary
            response['length'] = length
            response['width'] = width

            # Save Image
            cv2.imwrite(
                f"{TEMP_DIR}/{filename.split('.')[0]}_detected.{filename.split('.')[1]}", resized_image)

        except Exception as e:
            print("Exception: ", e)

        return response
