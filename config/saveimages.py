from fastapi import UploadFile

def saveimage(file: UploadFile):
    data = file.file.read()
    url = "static/imgs/" + file.filename.replace(" ", '').lower() + '.avif'
    with open(url, 'wb') as f:
        f.write(data)
    file.file.close()