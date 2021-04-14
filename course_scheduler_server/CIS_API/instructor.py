class Instructor:
    """
    Instructor structure
    """
    first_name: str
    last_name: str
    def __init__(self, first_name, last_name):
        """
        Initialization
        :param first_name: instructor's first name
        :param last_name: instructor's last name
        """
        self.first_name = first_name
        self.last_name = last_name

    def instructor_to_dict(self):
        """
        :return: convert an Instructor object to a dict
        """
        return {
            'first_name': self.first_name,
            'last_name': self.last_name
        }
