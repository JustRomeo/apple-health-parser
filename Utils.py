class Utils:

    # Files
    def readFile(path: str):
        data: list = []

        try:
            f = open(path, "r")
            data = f.read()
            f.close()
        except Exception as e:
            print("Error:", e)
        return data

    # Jsons
    def saveinFile(filepath: str, data: dict):
        with open(filepath, 'w+') as f:
            json.dump(data, f)
