from flask import Flask, render_template, request
from torbjorn import TagParser

app = Flask(__name__)

# Our main route.
@app.route("/",methods=['GET','POST'])
def main():

    # By default our url string is nothing.
    url_str = 'file:///Users/billy.grissom/Code/slackTest/tests/large.html'
    if request.method == 'POST':
        url_str = request.form['user_url']

    # Parse our URL.
    parser = TagParser(url_str)

    # Get our list of tag names.
    html_tags  = list()
    for tag_name in parser.tag_names:
        tag_count = parser.get_tag_count(tag_name)
        tag_highlights = sorted(parser.get_tag_idxs(tag_name))  # It looks like the highlight plugin needs to have the indices sorted, otherwise weird highlighting will ensue.
        html_tags.append(dict(name=tag_name,count=tag_count,highlights=tag_highlights))

    # Render the page and pass our variable.
    return render_template('index.html', html_url=parser.url, html_doc=parser.html, html_tags=html_tags,url_str=parser.url)

# Run our app when this file is called.
if __name__ == "__main__":
    # TODO: Switch this from debug mode before releasing!  This allows us to refresh the page without resetting Flask each time.
    app.run(debug=True)
