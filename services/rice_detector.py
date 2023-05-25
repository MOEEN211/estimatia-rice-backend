import cv2
from constants.constants import TEMP_DIR
from utils.utils import calc_avg_from_list_of_dicts
import math

# Define the height and width of the image in centimeters
IMAGE_HEIGHT_CM = 14.5
IMAGE_WIDTH_CM = 10.5


class HomogeneousBgDetector():
    def __init__(self):
        pass

    def detect(self, filename):
        file_path = str(TEMP_DIR / filename)
        response = {'short_rice_data': [],
                    'long_rice_data': [],
                    'short_rice_count': 0,
                    'long_rice_count': 0
                    }
        # Load the image
        img = cv2.imread(file_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)

        # Apply a fixed threshold value to the image
        _, thresh_img = cv2.threshold(blur, 210, 255, cv2.THRESH_BINARY)

        # Find contours in the thresholded image
        contours, hierarchy = cv2.findContours(
            thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the length and width of each rice grain in centimeters
        short_rice_count = 0
        long_rice_count = 0
        for contour in contours:
            # Calculate the area of the contour
            area = cv2.contourArea(contour)

            # Calculate the length and width of the contour
            rect = cv2.minAreaRect(contour)
            (x, y), (w, h), angle = rect
            if w < h:
                w, h = h, w
                angle += 90
            length = w  # Swap width and length variables
            width = h  # Swap width and length variables

            # Convert the length and width from pixels to centimeters
            length_cm = (length / img.shape[0]) * IMAGE_HEIGHT_CM
            width_cm = (width / img.shape[1]) * IMAGE_WIDTH_CM

            # Set a threshold value to separate short and long rice
            if 0.41 <= length_cm <= 2.0 and width_cm <= 0.3:
                if length_cm < 0.5:
                    # Draw contours around short rice in red color
                    cv2.drawContours(img, [contour], -1, (0, 0, 255), 3)
                    cv2.putText(img, f'Length: {length_cm:.2f} cm', (contour[0][0][0], contour[0][0][1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(img, f'Width: {width_cm:.2f} cm', (contour[0][0][0], contour[0][0][1] - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

                    response['short_rice_data'].append(
                        {'length': length_cm, 'width': width_cm})
                    short_rice_count += 1

                elif length_cm >= 0.5:
                    # Draw contours around long rice in green color
                    cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)
                    cv2.putText(img, f'Length: {length_cm:.2f} cm', (contour[0][0][0], contour[0][0][1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.putText(img, f'Width: {width_cm:.2f} cm', (
                        contour[0][0][0], contour[0][0][1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    response['long_rice_data'].append(
                        {'length': length_cm, 'width': width_cm})
                    long_rice_count += 1

        response['short_rice_count'] = short_rice_count
        response['long_rice_count'] = long_rice_count

        # Let's find average length

        avg_len_width_short_rice = calc_avg_from_list_of_dicts(
            response['short_rice_data'])
        avg_len_width_long_rice = calc_avg_from_list_of_dicts(
            response['long_rice_data'])

        total_grains = short_rice_count + long_rice_count
        response['avg_length'] = (
            avg_len_width_short_rice['length'] + avg_len_width_long_rice['length']) / total_grains if total_grains != 0 else 0
        response['avg_width'] = (
            avg_len_width_short_rice['width'] + avg_len_width_long_rice['width']) / total_grains if total_grains != 0 else 0

        # Show the total number of rice grains on the image
        cv2.putText(img, f'Total Short Rice Grains: {short_rice_count}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img, f'Total Long Rice Grains: {long_rice_count}', (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        img = cv2.resize(img, [1000, 1000])

        # Save Image
        # Finally we will save image
        cv2.imwrite(
            f"{TEMP_DIR}/{filename.split('.')[0]}_detected.{filename.split('.')[1]}", img)
        return response
