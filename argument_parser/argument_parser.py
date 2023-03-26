import argparse

class ArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('file', help='Url to file local path to an audio or video file')
        self.file = parser.parse_args().file

    def get_file(self):
        return self.file