# Torbjorn - An HTML Tag Viewer
This is my solution for a Slack coding challenge.  You can see a [live demo of it here](https://torbjorn.herokuapp.com/).


**Note: Demo might be slow on first launch.**  This is because it is being hosted on a free Heroku account which will sleep the app if it's [been inactive for 30 minutes](https://devcenter.heroku.com/articles/free-dyno-hours).

For more information on how this web-app works, check out the readme.html in this project or [here](https://torbjorn.herokuapp.com/about/).

##### Running Locally
If you have issues with the live demo, you can also run this app locally.  To do so, you'll need python installed and I'd recommend using a (virtualenv)[http://docs.python-guide.org/en/latest/dev/virtualenvs/].

Instructions:
```
pip install -r requirements.txt
python app/app.py
```

The app should now be running at: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)