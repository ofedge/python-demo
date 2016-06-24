import zipfile
import os


# zip the file in path folder with name filename
def zip_file(filename, path):
    f = zipfile.ZipFile(filename, 'w')
    write_zip(f, path)
    f.close()


# recursion write folder to zip_file
def write_zip(zip_file, path):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            zip_file.write(os.path.join(path, file))
            write_zip(zip_file, os.path.join(path, file))
        else:
            zip_file.write(os.path.join(path, file))

if __name__ == '__main__':
    filename = 'c:/users/silcata/desktop/myzip.zip'
    folder = 'c:/users/silcata/desktop/python'
    zip_file(filename, folder)
