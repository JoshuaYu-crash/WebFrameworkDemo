from Jlask.app import Jlask, render_template, req
import os

app = Jlask()

def Hello(request):
    return "Hello World"
app.add_url_rule(rule='/', view_func=Hello, methods=['GET'])


def World(request):
    return app.redirect('/')
app.add_url_rule(rule='/test', view_func=World, methods=['GET'])


def Render(request):
    name = request.args.get('name', 'World')
    return render_template(os.path.dirname(__file__), 'test1.html', name=name)
app.add_url_rule(rule='/render', view_func=Render, methods=['GET'])

def Form(request):
    m = req(request)
    if request.method == 'POST':
        print(m.formdata())
        return app.redirect('/form')
    return render_template(os.path.dirname(__file__), 'test2.html')
app.add_url_rule(rule="/form", view_func=Form)



if __name__ == '__main__':
    app.run()