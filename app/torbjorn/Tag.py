from LogObj import LogObj

class Tag(LogObj):

    def __init__(self,tag_str,start_idx,end_idx):
        """
        Represents a Tag in our html document.

        :param tag_str: String that we're going to parse into a tag object.
        :param start_idx: The starting index of the string in our document's massive string.
        :param end_idx: The end index of the string in our document's massive string.

        :type tag_str: str
        :type start_idx: int
        :type end_idx:   int
        """

        # Define our variables.
        self.start_idx = -1
        """:type: int"""

        self.end_idx = -1
        """:type: int"""

        self.name = ""
        """:type: str"""

        # Now, set our idxs.
        self.start_idx = start_idx
        self.end_idx = end_idx

        # Determine what the name of our tag is from the tag_str.
        self.name = tag_str[1:]
        ending_chars = [" ","/",">"]
        for char in ending_chars:
            char_idx = self.name.find(char)
            if char_idx != -1:
                self.name = self.name[:char_idx]

        # Log some info about what we parsed.
        self.logger.debug("[%d,%d] -> %s" % (start_idx, end_idx, tag_str))