class Date:

    def __init__(self, day, month):
        self.day = day
        self.month = month

    @property
    def date(self):
        return "/".join([self.day, self.month])
