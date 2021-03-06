from torbjorn import app
from flask import render_template, request, redirect, url_for, Response
from tagparser import TagParser
import json

@app.route('/api/getTags', methods=['GET', 'POST'])
def get_tags():

    # Define the variables we need.
    url_str = ""  # URL that we're going to parse, on launch this is nothing.  User sets this on the page.
    parser = None  # Parser object that fetches our tags from the page at the url provided.
    html_doc = ""  # The actual string that represents the doc.
    html_tags = list()  # List of tags that our parser found in the document.

    if request.method == 'POST':
        request_json = request.form.to_dict()
        url_str = request_json['url']

    # If this is a post, then grab the URL string that the user posted.
    try:
        parser = TagParser(url_str)
    except IOError:
        parser = None

    # If we were able to parse, then let's grab our list of tags that were parsed and pass them to our html template.
    total_tags = 0  # Keep track of how many occurrences of tags were found in general.
    if parser:
        html_doc = parser.html
        for tag_name in parser.tag_names:
            tag_count = parser.get_tag_count(tag_name)
            tag_highlights = sorted(parser.get_tag_idxs(tag_name)) # Highlight plugin needs to have the indices sorted, otherwise weird highlighting will ensue.
            total_tags += len(tag_highlights)
            html_tags.append(dict(name=tag_name, count=tag_count, highlights=tag_highlights))

    # Sort our list of tags based on whom is the most populated.
    html_tags.sort(key=lambda tag: tag["count"], reverse=True)

    # Now let's handle our alert text in the rendered template.
    alert_str = ""  # If set, the HTML doc will render this text in an alert.
    alert_style = ""  # If set, then the alert will be styled as if there was an error.
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
            alert_str = "Found %d unique tags with %d occurrences!" % (len(html_tags), total_tags)
            alert_style = "alert-success"

    result = dict()
    result["url_str"]   = url_str
    result["html_str"]  = html_doc
    result["html_tags"] = html_tags
    result["alert"]     = {"style": alert_style, "msg": alert_str}

    return Response(
        json.dumps(result),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/readme/')
def readme():
    return render_template('readme.html')

@app.route('/tests/test')
def test_small():
    return render_template('tests/test.html')

@app.route('/tests/no_tags')
def test_no_tags():
    return render_template('tests/no_tags.html')

@app.route('/tests/one_tag')
def test_one_tag():
    return render_template('tests/one_tag.html')

# Run our app when this file is called.
if __name__ == "__main__":
    # TODO: Switch this from debug mode before releasing!  This allows us to refresh the page without resetting Flask each time.
    app.run(debug=True)
