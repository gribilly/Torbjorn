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
            <div className="well well-lg">
                <textarea disabled id="html-doc" value={this.props.html} />
            </div>
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

        // Only display our list of tags if we actually have some tags to display.
        var tagList;
        if (this.props.tags.length > 0) {
            tagList =
                <div className="col-sm-3 sidebar">
                    <TagList tags={this.props.tags} handleClickTag={this.handleClickTag} />
                </div>;
        }

        // We only display our HtmlViewer if we have code to display.  In addition, we adjust its sizing depending on if we're also showing our tags or not.
        var htmlViewer;
        if (this.props.html) {
            htmlViewer =
                <div className={((this.props.tags.length > 0) ? "col-sm-9" : "col-sm-12") + " content"}>
                    <HtmlViewer html={this.props.html} highlights={this.state.highlights} />
                </div>;
        }

        return (
            <div className="row top-buffer">
                {tagList}
                {htmlViewer}
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
                        <h1>Torbjörn (React Version)</h1>
                    </a>
                    <p>
                        <small><i>"Build 'em up, Break 'em down!"</i></small>
                    </p>
                    <p>
                        Displays a summary of the HTML tags at a url.
                    </p>
                    <form method="post" className="submit-once" onSubmit={this.handleSubmit}>
                        <div className="input-group input-group-lg">
                            <input type="text" className="form-control" placeholder={(this.props.url) ? this.props.url : "Enter a url..." } value={this.state.url} onChange={this.handleInputChange} />
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

    getUrlParameter: function(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    },

    componentDidMount: function() {
        var url_param = this.getUrlParameter('url');
        if (url_param) {
            this.handleUrlSubmit({url: url_param})
        }
    },

    // Send our URL to our server's API for parsing.
    handleUrlSubmit: function(post_data) {
        $.ajax({
            url: this.props.api,
            dataType: 'json',
            type: 'POST',
            data: post_data,
            success: function(response) {
                this.setState({html: response.html_str, tags: response.html_tags, alert: response.alert, url: post_data.url});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.api, status, err.toString());
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
                <UrlForm onUrlSubmit={this.handleUrlSubmit} url={this.state.url} />
                {alert}
                <TagViewer tags={this.state.tags} html={this.state.html} />
            </div>
        );
   }
});

ReactDOM.render(
    <Torbjorn api="/api/getTags" />,
    document.getElementById('react-content')
);