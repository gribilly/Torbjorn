from flask import Flask, render_template, request, redirect, url_for
from urllib import FancyURLopener
import re

from torbjorn import TagParser

app = Flask(__name__)

# Our main route.
@app.route("/")
def main():
    # Use our parser to get the Tags out of an html doc.
    parser = TagParser('file:///Users/billy.grissom/Code/slackTest/tests/large.html')

    # Get our list of tag names.
    tag_tallies  = list()
    for tag_name in parser.tag_names:
        tag_count = parser.get_tag_count(tag_name)
        tag_highlights = sorted(parser.get_tag_idxs(tag_name))  # It looks like the highlight plugin needs to have the indices sorted, otherwise weird highlighting will ensue.
        tag_tallies.append(dict(name=tag_name,count=tag_count,highlights=tag_highlights))

    # Render the page and pass our variable.
    return render_template('index.html', html_url=parser.url, html_doc=parser.html, tag_tallies=tag_tallies,url_str=parser.url)

# Run our app when this file is called.
if __name__ == "__main__":
    # TODO: Switch this from debug mode before releasing!  This allows us to refresh the page without resetting Flask each time.
    app.run(debug=True)