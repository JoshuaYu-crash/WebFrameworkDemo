from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule
from jinja2 import PackageLoader, Environment, FileSystemLoader
import os

class Jlask(object):
    # 初始化url_map和存储endpoint对应视图函数
    url_map = Map([])
    endpoint_dict = {}

    def dispatch_request(self, request):
        print(self.url_map)
        url = request.path
        print(url)
        urls = self.url_map.bind(request.host)
        endpoint = urls.match(path_info=url)[0]
        view_func = self.endpoint_dict[endpoint](request)
        if isinstance(view_func, str):
            return Response(view_func)
        else:
            return view_func

    def wsgi_app(self, environ, start_response):
        # 启动
        # 实例化request，存入environ
        request = Request(environ)
        # 解析url，返回对应的视图函数
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        # 调用到wsgi_app，来执行url对应视图函数
        return self. wsgi_app(environ, start_response)


    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        methods = options.pop('methods', None)
        # 如果没有定义endpoint，就用试图函数的名字
        if endpoint is None:
            endpoint = view_func.__name__
            # 生成rule
            # rule： 定义的路由
            self.url_map.add(Rule(rule, endpoint=endpoint, methods=methods))
            # 存储endpoint对应的视图函数
            self.endpoint_dict[endpoint] = view_func
            # print(self.endpoint_dict)
            # print(self.url_map)

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def run(self, host=None, port=None, **options):
        if host is None:
            host = '127.0.0.1'
        if port is None:
            port = 5000
        # 注意第三个参数是自己，自己是一个可调用的类
        run_simple(host, port, self, **options)


    def redirect(self, request, path):
        urls = self.url_map.bind(request.host)
        endpoint = urls.match(path_info=path)[0]
        view_func = self.endpoint_dict[endpoint](request)
        if isinstance(view_func, str):
            return Response(view_func)
        else:
            return view_func


def render_template(path, template, **kwargs):
    template_path = os.path.join(path, 'templates')
    print(template_path)
    jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
    t = jinja_env.get_template(template)
    return Response(t.render(kwargs), mimetype='text/html')



app = Jlask()


# def Hello(request):
#     return "Hello World"
# app.add_url_rule(rule='/', view_func=Hello, methods=['GET'])


if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app)