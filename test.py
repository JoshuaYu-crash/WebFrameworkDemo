from Jlask.app import Jlask

app = Jlask()

def Hello(request):
    return "Hello World"
app.add_url_rule(rule='/', view_func=Hello, methods=['GET'])

app.run()