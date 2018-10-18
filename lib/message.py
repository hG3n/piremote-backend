class Message():
    def __init__(self):
        self.method = None
        self.success = False
        self.data = None

    def from_dict(self, obj):
        self.__dict__ = obj

    def __str__(self):
        return "Message \n" \
               "  > method : {0}\n" \
               "  > success: {1}\n" \
               "  > message: {2}" \
            .format(self.method, self.success, self.data)
