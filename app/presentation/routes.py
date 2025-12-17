from quart import render_template, request


async def index():
    client_addr = request.headers.get('X-Real-IP', request.remote_addr)
    return await render_template('index.html', client_addr=client_addr)
