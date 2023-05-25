import os
from functools import reduce
from datetime import datetime, timedelta


def get_unique_file_name(filename):
    """
    Given a filename, this function returns a unique filename by appending
    a number to the end of the filename if it already exists.
    """
    if not os.path.exists(filename):
        # If the file does not exist, return the original filename
        return filename

    # If the file already exists, add a number to the end until we find a unique filename
    i = 1
    while True:
        base, extension = os.path.splitext(filename)
        new_filename = f"{base}_{i}{extension}"
        if not os.path.exists(new_filename):
            return new_filename
        i += 1


def delete_tmp_images():
    # define the path to the tmp folder
    tmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')

    # get the current time
    now = datetime.now()

    # loop through all the files in the tmp folder
    for filename in os.listdir(tmp_path):
        file_path = os.path.join(tmp_path, filename)

        # check if the file is an image and if it's older than 1 hour
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.gif'):
            mod_time = os.path.getmtime(file_path)
            mod_datetime = datetime.fromtimestamp(mod_time)
            age = now - mod_datetime

            if age > timedelta(hours=1):
                os.remove(file_path)
                print(f"{filename} deleted from tmp folder.")

    print("All tmp images deleted.")


def save_image(path, data, b64=False):
    with open(path, 'wb') as f:
        if b64:
            f.write(data)
        else:
            for chunk in data:
                f.write(chunk)


# Function to sum the 'length' and 'width' values of two dictionaries
def calc_sum(rect1, rect2):
    return {'length': rect1['length'] + rect2['length'], 'width': rect1['width'] + rect2['width']}


def calc_avg_from_list_of_dicts(data):
    if len(data) == 0:
        return {'length': 0, 'width': 0}
    return reduce(calc_sum, data)
