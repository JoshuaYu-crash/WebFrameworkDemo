from Jlask.app import Jlask

app = Jlask()

def Hello(request):
    return "Hello World"
app.add_url_rule(rule='/', view_func=Hello, methods=['GET'])


def World(request):
    return app.redirect(request, '/')
app.add_url_rule(rule='/test', view_func=World, methods=['GET'])


if __name__ == '__main__':
    app.run()