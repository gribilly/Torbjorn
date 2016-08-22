from flask import Flask, render_template, request, redirect, url_for
from torbjorn import TagParser

app = Flask(__name__)

# Our main route.
@app.route("/",methods=['GET'])
def main():

    # Define the varaibles we need.
    url_str     = ""        # URL that we're going to parse, on launch this is nothing.  User sets this on the page.
    parser      = None      # Parser object that fetches our tags from the page at the url provided.
    html_doc    = ""        # The actual string that represents the doc.
    html_tags   = list()    # List of tags that our parser found in the document.

    url_str = request.args.get('url',"")

    # If this is a post, then grab the URL string that the user posted.
    try:
        parser = TagParser(url_str)
    except IOError:
        parser = None

    # If we were able to parse, then let's grab our list of tags that were parsed and pass them to our html template.
    total_tags = 0  # Keep trag of how many occurrences of tags were found in general.
    if parser:
        html_doc = parser.html
        for tag_name in parser.tag_names:
            tag_count = parser.get_tag_count(tag_name)
            tag_highlights = sorted(parser.get_tag_idxs(tag_name))  # It looks like the highlight plugin needs to have the indices sorted, otherwise weird highlighting will ensue.
            total_tags += len(tag_highlights)
            html_tags.append(dict(name=tag_name,count=tag_count,highlights=tag_highlights))

    # Sort our list of tags based on whom is the most populated.
    html_tags.sort(key=lambda tag: tag["count"], reverse=True)

    # This is used to populate the placeholder text of the input-field with whatever the user provided, if they provided nothing then we ask them to.
    url_input_str = url_str
    if not url_input_str:
        url_input_str = "Enter a URL..."

    # Now let's handle our alert text in the rendered template.
    alert_str   = ""    # If set, the HTML doc will render this text in an alert.
    alert_style = ""    # If set, then the alert will be styled as if there was an error.
    if url_str:
        if not parser:
            alert_str = "Invalid URL!"
            alert_style = "alert-danger"
        elif len(html_tags) == 0:
            alert_str = "No tags found!"
            alert_style = "alert-warning"
        # Grammar handling for if we have 1 tag.
        elif len(html_tags) == 1:
            alert_str = "Found %d unique tag!" % (len(html_tags))
            alert_style = "alert-success"
        else:
            alert_str = "Found %d unique tags with %d occurrences!" %(len(html_tags),total_tags)
            alert_style = "alert-success"

    # Render the page and pass our variable.
    return render_template('index.html', html_doc=html_doc, html_tags=html_tags, url_str=url_str, url_input_str=url_input_str, alert_str=alert_str, alert_style=alert_style)

@app.route('/',methods=['POST'])
def main_post():
    url_str = request.form['user_url']
    return redirect(url_for('main',url=url_str))

@app.route('/readme/')
def readme():
    return render_template('readme.html')

@app.route('/tests/test')
def test_small():
    return render_template('tests/test.html')

@app.route('/tests/no_tags')
def test_no_tags():
    return render_template('tests/no_tags.html')

# Run our app when this file is called.
if __name__ == "__main__":
    # TODO: Switch this from debug mode before releasing!  This allows us to refresh the page without resetting Flask each time.
    app.run(debug=True)
