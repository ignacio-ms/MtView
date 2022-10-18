from app import values


class efp:

    def __init__(self):
        self.paths = []
        self.labels = []

    @staticmethod
    def init_colors():
        """
        Initializes all tissue fills color to white
        """

        return {label+'_fill': '#ffa400' for label in values.img_labels}
