import os
import socketserver
import json

todo_list = []

class RequestHandler(socketserver.BaseRequestHandler):
  def handle(self):
    print('Receive connection from ' + str(self.client_address))
    req = self.request.recv(1024).decode()
    req = json.loads(req)

    command = req['command']
    data = req['data']

      
    if command == 'view':
      res = {
        'ok': True,
        'msg': 'Success',
        'data': todo_list
      }
    elif command == 'add':
      todo_list.append({
        'desc': data['desc'],
        'date': data['date'],
        'id' : data['id']
      })
      res = {
        'ok': True,
        'msg': 'Success',
        'data': None
      }
        
    elif command == 'delete':
      for i, item in enumerate(todo_list.copy()):
          if item['id'] == data['id']:
              todo_list.pop(i)
      res = {
        'ok': True,
        'msg': 'Success',
        'data': None
      }
        
    else: 
      res = {
        'ok': False,
        'msg': 'Invalid Command.',
        'data': None
      }
    res = json.dumps(res).encode()
    self.request.sendall(res)

  def finish(self):
    save_data()

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def load_data():
    global todo_list
    if not os.path.exists('data.json'):
        return
    with open('data.json') as f:
        todo_list = json.loads(f.read())


def save_data():
    with open('data.json', 'w') as f:
        f.write(json.dumps(todo_list))


load_data()
server = Server(('localhost', 1717), RequestHandler)
print('Listening on port 1717...')
server.serve_forever()
