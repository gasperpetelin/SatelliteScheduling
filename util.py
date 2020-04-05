import json


class ProblemLogger:
    def __init__(self, file, header):
        self.file = file
        self.write_header = True
        self.header = header

    def log(self, instance):
        f = open(self.file, "a+")
        if self.write_header:
            self.write_header = False
            f.write(self.header + '\n')
        f.write(json.dumps(instance) + '\n')
        f.close()
