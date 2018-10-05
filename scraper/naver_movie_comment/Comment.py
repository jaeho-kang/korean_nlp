class MovieComment:
    def __init__(self):
        self.no = -1
        self.movie_name = ""
        self.comment = ""
        self.score = -1

    @property
    def str(self):
        return "{}:{}\n{}\n{}".format(self.no, self.movie_name, self.comment, self.score)

    @property
    def dict(self):
        data = {}
        data["no"] = self.no
        data["movie_name"] = self.movie_name
        data["comment"] = self.comment
        data["score"] = self.score
        return data
