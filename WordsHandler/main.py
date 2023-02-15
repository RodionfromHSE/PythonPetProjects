from GlobalHandler import GlobalHandler


if __name__ == '__main__':
    filename = "data.json"
    handler = GlobalHandler(filename)
    handler.extract_and_add()
