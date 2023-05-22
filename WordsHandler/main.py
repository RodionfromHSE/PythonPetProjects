from GlobalHandler import GlobalHandler


if __name__ == '__main__':
    filename = r"C:\Users\rodio\Programming\Python\PythonPetProjects\WordsHandler\data.json"
    handler = GlobalHandler(filename)
    handler.extract_and_add()
    if input("Clear? (y/n)") == 'y':
        handler.clear()
