import prometheus_client
from requests.exceptions import ConnectionError
from wsgiref.simple_server import make_server
from prometheus_client import Summary, Gauge, make_wsgi_app, CollectorRegistry
import time
import requests

registry=CollectorRegistry()
up_metric = Gauge("sample_external_url_up","Metric to check availability of external url", ['url'], registry=registry)
response_time_metric = Gauge("sample_external_url_response_ms","Metric to measure response time of external url", ['url'], registry=registry)
response_latency_metric = Summary("sample_external_url_response_latency_ms","Metric to measure response latency of external url", ['url'], registry=registry)

def my_app(environ, start_fn):
    service = ['https://httpstat.us/200', 'https://httpstat.us/503']
    if environ['PATH_INFO'] == '/':
        headers = [('Content-type', 'html')]
        for s in service:
            try:
                start = time.time()
                res = requests.get(s)
                end = time.time()
                response_latency_metric.labels(s).observe(end - start)
                response_time_metric.labels(s).set(res.elapsed.total_seconds()/1000)
            except ConnectionError as e:
                start_fn('406 Bad Connection', headers)
                return [b'Connection Error while accessing Sample URLS']
            except Exception as e: 
                 start_fn(res.status_code, headers)
                 return [b'Issue while accessing Sample urls']
            if res.status_code == 200:
                up_metric.labels(s).set(int(1))
            else:
                up_metric.labels(s).set(int(0))

    if environ['PATH_INFO'] == '/metrics':
        metrics_app = make_wsgi_app(registry)
        return metrics_app(environ, start_fn)
    
    headers = [('Content-type', 'html')]
    start_fn('200 OK', headers)
    return [b'<h1><span style="color: #0000ff; background-color: #ffffff;">This page when accessed checks the following sample urls Availability and Response times and exposes the prometheus metrics in /metrics endpoint</span></h1> \
<h1><a href="https://httpstat.us/503" target="_blank">https://httpstat.us/503</a>&nbsp;</h1> \
<h1><a href="https://httpstat.us/200" target="_blank">https://httpstat.us/200</a></h1>']
    

if __name__ == '__main__':
    httpd = make_server('', 2080, my_app)
    httpd.serve_forever()
