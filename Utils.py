class Utils:

    def readFile(path: str):
        data: list = []

        try:
            f = open(path, "r")
            data = f.read()
            f.close()
        except Exception as e:
            print("Error:", e)
        return data
