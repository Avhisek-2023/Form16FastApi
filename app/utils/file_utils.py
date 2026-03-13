import os


def save_uploaded_file(file, folder):

    os.makedirs(folder, exist_ok=True)

    filepath = os.path.join(folder, file.filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return filepath