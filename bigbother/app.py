#!/usr/bin/env python

from flask import Flask
from flask_graphql import GraphQLView

from .db import Session, init_db
from .schema import schema

app = Flask(__name__)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


if __name__ == '__main__':
    init_db()
    app.run()
