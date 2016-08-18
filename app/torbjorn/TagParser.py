from urllib import FancyURLopener
from urlparse import urlparse
from bs4 import BeautifulSoup
from LogObj import LogObj
from Tag import Tag

class TagParser(LogObj):

    def __init__(self,url=""):
        """
        Provided a url this will load the HTML source, make it pretty, and parse a list of tags from it.
        """

        # Private. Our URL that we want to grab the html source of.
        self.__url = ""
        """:type: str"""

        # Private. The string representing the contents of our HTML doc.  We set this when we load our url.
        self.__html = ""
        """:type: str"""

        # Public. Our dictionary that contains all of our tags.  We map a tag name to a list of Tag objects.
        self.__tags = dict()
        """:type: dict[str,list[Tag]]"""

        # If the user passed in a string, then set our url
        if url:
            self.url = url

    @property
    def html(self):
        """
        The string that represents the html that be at our url.

        :rtype: str
        """
        return self.__html

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self,url):
        """
        Sets our url, grabs the html, and then parses it so that we populate our tags dictionary.

        :param url: String representing the url.  If a given scheme isn't detected in the url, (i.e. 'http://' or 'file://') then we'll assume we're dealing with 'http://'.
        :type  url: str
        """
        if not urlparse(url).scheme:
            url = "http://" + url
        self.__url = url

        # Now that we've got our url, let's fetch the html.
        raw_html = FancyURLopener().open(url).read()

        # Use soup to format the html so that it's pretty.
        soup = BeautifulSoup(raw_html, 'html.parser')
        self.__html = soup.prettify()

        # Now let's parse our HTML for Tags.
        self.__parse(self.__html)

    @property
    def tag_names(self):
        """
        Helper function that returns a list of the name of the tags found in our html.  This is the same as returning a list of the keys.

        :return:
        """
        return self.__tags.keys()

    def get_tag_idxs(self, tag_name):
        """
        Provided the name of a tag, this will return a list where each entry is a list with the start and end idx of the tag in our original html string.

        If we cannot find the tag_name that was provided in our dictionary, then a KeyError exception is raised.

        :param tag_name: Name of the tag that we want to fetch a list for.
        :type  tag_name: str
        :return: list[list[int]]
        """
        idx_list = list()
        for tag in self.__tags[tag_name]:
            idx_list.append([tag.start_idx, tag.end_idx])
        return idx_list

    def get_tag_count(self, tag_name):
        """
        Provided the name of a tag, this will return a the number of times the tag occurs in our url.

        If we cannot find the tag_name that was provided in our dictionary, then a KeyError exception is raised.

        :param tag_name: Name of the tag that we want to fetch a list for.
        :type  tag_name: str
        :return: list[list[int]]
        """
        return len(self.__tags[tag_name])


    def __parse(self,html_doc):
        """
        Private method that parses an string for HTML tags, and populates our tags dictionary with its findings.

        :param html_doc: String that represents the html_doc we want to parse.
        :type  html_doc: str
        """

        # Clear our tags dictionary since we're loading a new URL.
        self.__tags = dict()

        # Iterate through our source code char by char so that we can build up a list of tags.
        may_have_tag = False
        in_tag = False
        tag_str = ""
        tag_idx = 0

        print html_doc

        for idx,char in enumerate(html_doc):

            # Triggered when the last char we ran into was a '<'.
            if may_have_tag:
                # If this char is an alpha, then we've got a tag!
                if char.isalpha():
                    tag_str += char
                    in_tag = True
                # If this char isn't an alpha, then this isn't a tag.
                else:
                    tag_str = ""
                may_have_tag = False
                continue

            # Triggered when we're in a tag, since we're in a tag we keep adding characters to our tag.
            if in_tag:
                tag_str += char
                # If we hit a '>' then we've reached the end of our tag.  This means that we'll need to add the tag to our list of tags.
                if char == ">":
                    self.__add_tag(Tag(tag_str, tag_idx, idx))
                    tag_str = ""
                    in_tag = False

            # If we hit a "<", then this may be the start of a tag!
            if char == "<":
                may_have_tag = True
                tag_str += char
                tag_idx = idx
                continue

        self.logger.info("Parsed %d tags" % len(self.__tags))

    def __add_tag(self,tag):
        """
        Private method that, provided a Tag object, adds it to our tags dictionary.  If a key for the tag doesn't already exist, then we'll create one.

        :param tag: Tag object that we want to add to our dictionary.
        :type  tag: Tag.Tag
        """
        if self.__tags.get(tag.name,None) == None:
            self.__tags[tag.name] = list()
        self.__tags[tag.name].append(tag)

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    thing = TagParser('file:///Users/billy.grissom/Code/slackTest/tests/test.html')


