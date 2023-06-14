# HTTP Server

This code implements a simple HTTP server that listens for client connections, processes HTTP requests, and serves requested files as responses. It supports GET requests and handles various HTTP response codes. The server is implemented in Python and uses sockets for network communication.

## Usage

To use the HTTP server, follow these steps:

1. Ensure you have Python installed on your system.
2. Save the code to a file with a `.py` extension (e.g., `http_server.py`).
3. Open a terminal or command prompt and navigate to the directory where the file is saved.
4. Run the server by executing the following command:

   ```bash
   python http_server.py -p <port> -d <root_directory>
   ```

   Replace `<port>` with the desired port number for the server to listen on, and `<root_directory>` with the path to the directory you want to serve files from.

## Command Line Arguments

The server accepts the following command line arguments:

- `-p` or `--port`: Specifies the port number for the server to listen on. It should be an integer between 1024 and 65535 (inclusive). If an invalid port number is provided, an error message will be displayed, and the server will exit.
- `-d` or `--root`: Specifies the root directory from which the server serves files. The path should be a valid directory on your system.

Example usage:

```bash
python http_server.py -p 8000 -d /path/to/root_directory
```

## Dependencies

The code requires the following Python modules:

- `argparse`: For parsing command-line arguments.
- `os`: For working with file paths and directories.
- `sys`: For printing error messages.
- `datetime`: For getting current time and date.
- `socket`: For creating and managing network sockets.
- `csv`: For writing server statistics to a CSV file.

## How It Works

1. The script parses the command-line arguments to get the desired port number and root directory.
2. It creates a socket and binds it to the specified port, then starts listening for incoming connections.
3. When a client connects, it accepts the connection and retrieves the client's request.
4. The script checks the HTTP version and responds with an error if it's not supported.
5. If the request method is not `GET`, an appropriate error response is sent.
6. If the requested file doesn't exist, a "404 Not Found" response is sent.
7. If the requested file is a directory, another "404 Not Found" response is sent.
8. If the requested file exists and is a valid file, its content is loaded and sent as the response.
9. The script determines the MIME type of the file based on its extension and includes it in the response headers.
10. Server statistics are logged to a CSV file (`1608636SocketOutput.csv`) for each request served.
11. The response headers and content are sent back to the client.
12. The connection is closed, and the server continues listening for new connections.


## HTTP Responses

The server handles the following HTTP response codes:

- `200 OK`: The requested file is found and successfully served as the response.
- `404 Not Found`: The requested file does not exist in the specified directory.
- `501 Not Implemented`: The HTTP request method other than GET is not supported.
- `505 HTTP Version Not Supported`: The server only supports HTTP/1.1.

The server logs each request and response in a CSV file (`1608636SocketOutput.csv`) and a text file (`1608636HTTPResponses.txt`), respectively.

## MIME Types

The server sets the appropriate MIME type for each file based on its extension. It supports a wide range of MIME types for common file formats.

## Closing the Server

To stop the server, press `Ctrl+C` in the terminal or command prompt where it is running. The server will gracefully close all active connections and then terminate.

## Additional Files

- `1608636HTTPResponses.txt`: This text file logs all the HTTP responses sent by the server.
- `1608636SocketOutput.csv`: This CSV file logs server statistics for each client request served. It includes information such as the 4-tuple (server IP, server port, client IP, client port), requested URL, HTTP response status, and bytes transmitted.

**Note:** Make sure the script is run with sufficient permissions to bind to the desired port and access the root directory.

**Warning:** Well-known port numbers (0-1023) are flagged with a warning message, as they are typically reserved for specific services. Use caution when choosing a port number within this range.

---

Note: This is a basic HTTP server implementation provided for educational purposes. It may not be suitable for production use due to its simplicity and lack of security measures.
