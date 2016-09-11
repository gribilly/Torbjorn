var HtmlViewer = React.createClass({

    onInput(input) {
        if (!this.props.highlights) {
            return [];
        }
        return this.props.highlights;
    },

    componentDidUpdate: function() {
        $(document.getElementById('html-doc')).highlightWithinTextarea(this.onInput);
    },

    render: function () {
        return (
            <textarea disabled id="html-doc" value={this.props.html} />
        );
    }
});

var TagListItem = React.createClass({

    handleClick: function(e) {
        this.props.handleClickTag(this);
    },

    render: function() {
        return (
            <a className="list-group-item" onClick={this.handleClick}>
                <span className="badge">
                    {this.props.count}
                </span>
                {this.props.name}
            </a>
        );
    }
});

var TagList = React.createClass({

    handleClickTag: function(tag) {
        this.props.handleClickTag(tag);
    },

    render: function() {
        // Iterate through our tags and generate a list item for each one.
        return (
            <div className="well well-lg">
                <div className="scrollable-menu">
                    <div className="list-group">
                        {this.props.tags.map(function(tag) {
                            return <TagListItem name={tag.name} count={tag.count} key={tag.name} highlights={tag.highlights} handleClickTag={this.handleClickTag} />
                        }, this)}
                    </div>
                </div>
            </div>
        );
    }
});

var TagViewer = React.createClass({

    getInitialState: function() {
      return {
          highlights: [],
      };
    },

    handleClickTag: function(tag) {
        console.log(tag.props.highlights);
        this.setState({highlights: tag.props.highlights});
    },

    render: function () {
        return (
            <div className="row top-buffer">
                <div className="col-sm-3 sidebar">
                    <TagList tags={this.props.tags} handleClickTag={this.handleClickTag} />
                </div>
                <div className="col-sm-9 content">
                    <div className="well well-lg">
                        <HtmlViewer html={this.props.html} highlights={this.state.highlights} />
                    </div>
                </div>
            </div>
        );
    }
});

var Alert = React.createClass({
    render: function () {
        var divStyle = {
                textAlign: "center",
                fontWeight: "bold"
        };
        return (
            <div className="row" >
                <div className="col-sm-12">
                    <div className={this.props.alertStyle} role="alert">
                        <div style={divStyle}><h3>{this.props.msg}</h3></div>
                    </div>
                </div>
            </div>
        );
    }
});

var UrlForm = React.createClass({

    getInitialState: function() {
      return {
          url: "",
          disabled: true
      };
    },

    handleInputChange: function(ele) {
        var url = ele.target.value;
        var url_trimmed = url.trim();

        if(url_trimmed == this.state.url) {
            return;
        }
        this.setState({url: url});
        if(!url_trimmed) {
            this.setState({disabled: true});
        }
        else {
            this.setState({disabled: false});
        }
    },

    handleSubmit: function(ele) {
        ele.preventDefault();
        var url = this.state.url.trim();
        if (!url) {
            return;
        }
        this.setState({url: this.state.url.trim()});
        this.setState({disabled: true});
        this.props.onUrlSubmit({url: url});
    },

    render: function() {
        var disabled = this.state.disabled ? 'disabled' : '';
        return (
            <div className="row">
                <div className="jumbotron">
                    <a href="readme/">
                        <h1>Torbjörn</h1>
                    </a>
                    <p>
                        <small><i>"Build 'em up, Break 'em down!"</i></small>
                    </p>
                    <p>
                        Displays a summary of the HTML tags at a url.
                    </p>
                    <form method="post" className="submit-once" onSubmit={this.handleSubmit}>
                        <div className="input-group input-group-lg">
                            <input type="text" className="form-control" placeholder="Enter a url..." value={this.state.url} onChange={this.handleInputChange} />
                            <span className="input-group-btn">
                                <button disabled={disabled} className={"btn btn-default" + disabled} id="btn-url" type="submit">View tags!</button>
                            </span>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
});

var Torbjorn= React.createClass({

    // Define our initial state for all of our variables.
    getInitialState: function() {
        return {
            alert: { style:"", msg:"" },
            tags:  [],
            html:  "",
            url:   ""
        };
    },

    // Send our URL to our server's API for parsing.
    handleUrlSubmit: function(post_data) {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: post_data,
            success: function(response) {
                this.setState({html: response.html_str, tags: response.html_tags, alert: response.alert});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    // Define how we'll render our app.
    render: function () {
        // Our alert renders based on whether or not we've got an alert to display.
        var alert;
        if (this.state.alert.msg) {
            alert = <Alert alertStyle={"alert " + this.state.alert.style} msg={this.state.alert.msg}/>;
        }

        return (
            <div className="container">
                <UrlForm onUrlSubmit={this.handleUrlSubmit} />
                {alert}
                <TagViewer tags={this.state.tags} html={this.state.html} />
            </div>
        );
   }
});

ReactDOM.render(
    <Torbjorn url="/api/getTags" />,
    document.getElementById('content')
);