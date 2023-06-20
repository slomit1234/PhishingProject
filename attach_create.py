def copy():
    file = open("attachment.py", "r")
    copy_file = open("copy_attachment.py", "w")
    copy_file.write(file.read())
    file.close()
    copy_file.close()

if __name__ == "__main__":
    copy()