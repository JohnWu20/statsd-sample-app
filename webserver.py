from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket
import json

class httpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/a':
            self.wfile.write('Helloa! '.encode())
        elif self.path == '/statsd':
            send_statsd_metrics()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            print(json.dumps({"traceId": "dummy"}).encode())
            self.wfile.write(json.dumps({"traceId": "dummy"}).encode())
        elif self.path == '/':
            self.send_response(200)
            self.end_headers()
        else:
            self.wfile.write('Hello! '.encode())

def send_statsd_metrics():
    os.environ['INSTANCE_ID'] = 'abcd'
    os.environ['COLLECTOR_UDP_ADDRESS'] = '127.0.0.1:55690'
    INSTANCE_ID = os.getenv('INSTANCE_ID')
    RECEIVER_ADDRESS = os.getenv('COLLECTOR_UDP_ADDRESS')
    print (INSTANCE_ID)
    print (RECEIVER_ADDRESS)
    if INSTANCE_ID is not None and RECEIVER_ADDRESS is not None:
        statsD_metric = bytes('statsdTestMetric1g_%s:1|g|#mykey1:myvalue1,OTelLib:abc\nstatsdTestMetric2g_%s:2|g|#mykey2:myvalue2,OTelLib:abc\nstatsdTestMetric3g_%s:3|g|#mykey3:myvalue3,OTelLib:abc\nstatsdTestMetric1c_%s:1|c|@0.25|#mykey1:myvalue1,OTelLib:abc\nstatsdTestMetric2c_%s:2|c|#mykey2:myvalue2,OTelLib:abc\nstatsdTestMetric3c_%s:3|c|#mykey3:myvalue3,OTelLib:abc' % (INSTANCE_ID, INSTANCE_ID, INSTANCE_ID, INSTANCE_ID, INSTANCE_ID, INSTANCE_ID),'utf-8')
        opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        opened_socket.sendto(statsD_metric, (RECEIVER_ADDRESS.split(':')[0], int(RECEIVER_ADDRESS.split(':')[1])))
    return

def main():
    ADDRESS = os.getenv('LISTEN_ADDRESS')
    if ADDRESS is not None:
        HOST = ADDRESS.split(':')[0]
        PORT = int(ADDRESS.split(':')[1])
    else:
        HOST = '0.0.0.0'
        PORT = 4321
    server = HTTPServer((HOST, PORT), httpHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()    