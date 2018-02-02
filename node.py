import http.server
import socketserver
import time
import threading
import random
import sys

FILE = '/Users/macbook/Dropbox/WORK/MinerStartup/NodeServer/node{}.txt'
if len(sys.argv) == 2:
    NODES = int(sys.argv[1])
else:
    NODES = 4


class MyHandler(http.server.BaseHTTPRequestHandler):
    # 0 failing
    # 1 working
    mode = 1
    nodeName = None
    filePath = None

    def do_GET(self):
        if self.mode == 1:
            with open(self.filePath) as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=UTF-8')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

    @classmethod
    def getHandler(cls, nodeName, mode, filePath):
        props = {
            'mode': mode,
            'filePath': filePath,
            'nodeName': nodeName
        }
        handlerClass = type("MyHandler{}".format(nodeName), (cls,), props)
        return handlerClass


if __name__ == "__main__":
    handlers = []
    for i in range(1, NODES+1):
        handler = MyHandler.getHandler('{:02}'.format(i),
                                       1,
                                       FILE.format(i))
        handlers.append(handler)
        port = 8000 + i
        httpd = socketserver.TCPServer(("", port), handler)
        print('Serving at', port)
        p = threading.Thread(target=httpd.serve_forever, daemon=True)
        p.start()

    while True:
        time.sleep(1)
        helpTxt = ('0 <number>: random <number> of nodes are off\n'
                   '1 [id1] [id2] ...: turn off nodes ID id1 id2\n'
                   '2 [id1] [id2] ...: turn on nodes ID id1 id2\n')
        print(helpTxt)
        s = input('Mode -> ')
        s = list(map(int, s.split(' ')))
        if s[0] == 0:
            allNodes = set(range(1, NODES+1))
            selectedNodes = set()
            for _ in range(s[1]):
                selectedNodes.add(random.choice(list(allNodes)))
                allNodes = allNodes - selectedNodes
            print('Selected nodes: ', ' '.join(map(str, selectedNodes)))
            for i in selectedNodes:
                # turn off
                handlers[i-1].mode = 0
        elif s[0] == 1:
            for i in s[1:]:
                handlers[i-1].mode = 0
        elif s[0] == 2:
            for i in s[1:]:
                handlers[i-1].mode = 1
        else:
            raise ValueError('Incorrect arguments')
