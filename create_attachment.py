def copy():
    file = open("attachment.py", "r")
    copy_file = open("copy_attachment.py", "w")
    copy_file.write(fp.read())
    file.close()
    copy_file.close()

if __name__ == "__main__":
    copy()