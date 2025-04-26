from flask import Flask, render_template, request, jsonify
import logging.config
import socket


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def proxy():
    try:
        print(request.files, flush=True)
        body = {kname: v.encode() for kname, v in request.form.items() }
        body.update({fname: d.read() for fname, d in request.files.items()})

        print(body, flush=True)

        if not body or 'target' not in body or 'data' not in body:
            return jsonify({'error': 'Expected keys: target, data'}), 400

        target = body['target']
        data = body['data']

        # split the target, assuming its in this format <HOST>:<PORT>
        try:
            host, port = target.split(b':')
            port = int(port)
        except ValueError:
            return jsonify({'error': 'Invalid target format. Use "host:port"'}), 400

        print(f"{host=} {port=}", flush=True)

        # proxy time!
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.settimeout(5)
            tcp_socket.connect((host, port))
            tcp_socket.sendall(data)
            tcp_socket.sendall(b"\n")

            return render_template("index.html", result=tcp_socket.recv(1024).decode().strip())

    except socket.error:
        return jsonify({'error': f'Socket error'}), 500


# The generative AI im using says this is how I can change my logging config on the fly ¯\_(ツ)_/¯
log_server = logging.config.listen(9000)
log_server.start()

app.run(host="0.0.0.0", port=8000)
