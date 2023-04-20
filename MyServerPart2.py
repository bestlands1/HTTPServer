import argparse
import os
import sys
import datetime
import socket
import csv

# Location of where server is located
home_dir = (os.getcwd())

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int)
parser.add_argument('-d', '--root', type=str)
arg = parser.parse_args()

# Make user Port equal to user port
SERVER_PORT = arg.port
SERVER_HOST = '127.0.0.1'
# Checks port number
if 1024 <= SERVER_PORT <= 65535:
    pass
elif 0 <= SERVER_PORT <= 1023:
    print("Warning: Well Known Port Detected")
else:
    print('Error: Invalid port number', file=sys.stderr)
    sys.exit()

# Print server information
print(f'{SERVER_PORT} entered port number, {arg.root} entered root directory path')

# setting directory thats specified by user
os.chdir(arg.root)

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print(f'Welcome socket created: {SERVER_HOST}, {SERVER_PORT}')

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Print connection request information
    print(f'Connection requested from {client_address[0]}, {client_address[1]}')

    # Get the client request
    request = client_connection.recv(1024).decode()
    print(request)

    if not request:
        # Ignore favicon
        continue

    request_parts = request.split()
    method = request_parts[0]
    path = os.path.join(os.getcwd(), request_parts[1][1:])
    version = request_parts[2]

    # Current Time
    current_time = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

    ##Check HTTP Version
    if version == 'HTTP/1.1':
        pass
    else:
        response_header = f'HTTP/1.1 505 HTTP Version Not Supported\r\nDate: {current_time}\r\n\r\n'
        response = (str(response_header))
        with open(os.path.join(home_dir, '1608636HTTPResponses.txt'), 'a+') as text:
            text.write(str(response))
        client_connection.sendall(response_header.encode())
        client_connection.close()

    # Check if request method is GET
    if method != 'GET':
        response_header = f'HTTP/1.1 501 Not Implemented\r\nDate: {current_time}\r\n\r\n'
        response = (str(response_header))
        with open(os.path.join(home_dir, '1608636HTTPResponses.txt'), 'a+') as text:
            text.write(str(response))
        client_connection.sendall(response_header.encode())
        client_connection.close()
        continue

    # Check if requested file exists
    if not os.path.exists(path):
        response_header = f'HTTP/1.1 404 Not Found\r\nDate: {current_time}\r\n\r\n'
        response = (str(response_header))
        with open(os.path.join(home_dir, '1608636HTTPResponses.txt'), 'a+') as text:
            text.write(str(response))
        client_connection.sendall(response_header.encode())
        client_connection.close()
        continue

    # Load requested file and send as response
    try:
        with open(path, 'rb') as f:
            content = f.read()
    except IsADirectoryError:
        response_header = f'HTTP/1.1 404 Not Found\r\nDate: {current_time}\r\n\r\n'
        response = (str(response_header))
        with open(os.path.join(home_dir, '1608636HTTPResponses.txt'), 'a+') as text:
            text.write(str(response))
        client_connection.sendall(response_header.encode())
        client_connection.close()
        continue

    MIME_TYPES = {
        ".aac": "audio/aac",
        ".abw": "application/x-abiword",
        ".arc": "application/x-freearc",
        ".avif": "image/avif",
        ".avi": "video/x-msvideo",
        ".azw": "application/vnd.amazon.ebook",
        ".bin": "application/octet-stream",
        ".bmp": "image/bmp",
        ".bz": "application/x-bzip",
        ".bz2": "application/x-bzip2",
        ".cda": "application/x-cdf",
        ".csh": "application/x-csh",
        ".css": "text/css",
        ".csv": "text/csv",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".eot": "application/vnd.ms-fontobject",
        ".epub": "application/epub+zip",
        ".gz": "application/gzip",
        ".gif": "image/gif",
        ".htm": "text/html",
        ".html": "text/html",
        ".ico": "image/vnd.microsoft.icon",
        ".ics": "text/calendar",
        ".jar": "application/java-archive",
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".js": "text/javascript",
        ".json": "application/json",
        ".jsonld": "application/ld+json",
        ".mid": "audio/midi",
        ".midi": "audio/midi",
        ".mjs": "text/javascript",
        ".mp3": "audio/mpeg",
        ".mp4": "video/mp4",
        ".mpeg": "video/mpeg",
        ".mpkg": "application/vnd.apple.installer+xml",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".oga": "audio/ogg",
        ".ogv": "video/ogg",
        ".ogx": "application/ogg",
        ".opus": "audio/opus",
        ".otf": "font/otf",
        ".png": "image/png",
        ".pdf": "application/pdf",
        ".php": "application/x-httpd-php",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".rar": "application/vnd.rar",
        ".rtf": "application/rtf",
        '.sh': 'application/x-sh',
        '.svg': 'image/svg+xml',
        '.tar': 'application/x-tar',
        '.tif': 'image/tiff',
        '.tiff': 'image/tiff',
        '.ts': 'video/mp2t',
        '.ttf': 'font/ttf',
        '.txt': 'text/plain',
        '.vsd': 'application/vnd.visio',
        '.wav': 'audio/wav',
        '.weba': 'audio/webm',
        '.webm': 'video/webm',
        '.webp': 'image/webp',
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.xhtml': 'application/xhtml+xml',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xml': 'application/xml',
        '.xul': 'application/vnd.mozilla.xul+xml',
        '.zip': 'application/zip',
        '.3gp': 'video/3gpp',
        '.3g2': 'video/3gpp2',
        '.7z': 'application/x-7z-compressed'
    }

    file_ext = os.path.splitext(path)[1]
    content_type = MIME_TYPES.get(file_ext, 'application/octet-stream')

    content_length = len(content)
    last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    response_http = ('HTTP/1.1 200 OK')
    response = f'{response_http}\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\nLast-Modified: {last_modified}\r\nDate: {current_time}\r\nConnection: close\r\n\r\n'
    response_header = f'{response_http}\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\nLast-Modified: {last_modified}\r\nDate: {current_time}\r\nConnection: close\r\n\r\n'.encode() + content

    with open(os.path.join(home_dir, '1608636SocketOutput.csv'), 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['Client request served', '4-Tuple:', SERVER_HOST, SERVER_PORT, client_address[0], client_address[1],
             'Requested URL', path, response_http, 'Bytes transmitted:', content_length])

    with open(os.path.join(home_dir, '1608636HTTPResponses.txt'), 'a+') as text:
        text.write(str(response))

    client_connection.sendall(response_header)

    # Print connection close information
    print(f'Connection to {client_address[0]}, {client_address[1]} is closed\n')
    client_connection.close()

# Close socket
server_socket.close()