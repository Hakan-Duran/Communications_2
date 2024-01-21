import socket

# Server configuration
SERVER_HOST = "127.0.0.1"
UPLOAD_PORT = 12345
DOWNLOAD_PORT = 12346
BUFFER_SIZE = 1024

# Function to handle file download
def download_file(client_socket):
    # Received file name which comes from client
    file_name = client_socket.recv(BUFFER_SIZE).decode()
    try:
        with open(file_name, "rb") as file:
            file_data = file.read()
            #Requested file is sending to the client
            client_socket.sendall(file_data)
            print(f"File '{file_name}' sent to the client")
    except FileNotFoundError:
        print(f"File '{file_name}' not found on the server")

# Create socket for file upload
upload_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
upload_socket.bind((SERVER_HOST, UPLOAD_PORT))
upload_socket.listen(1)  # Listen for one incoming connection

# Create socket for file download
download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
download_socket.bind((SERVER_HOST, DOWNLOAD_PORT))
download_socket.listen(1)

print(f"[*] Listening for file upload on {SERVER_HOST}:{UPLOAD_PORT}")
print(f"[*] Listening for file download on {SERVER_HOST}:{DOWNLOAD_PORT}\n")

# Accept connections for upload and download
upload_client_socket, upload_client_address = upload_socket.accept()
download_client_socket, download_client_address = download_socket.accept()

# Upload process
file_data = upload_client_socket.recv(BUFFER_SIZE)
file_name = "student_info.txt"
with open(file_name, "wb") as file:
    file.write(file_data)
print(f"File received and saved as {file_name}")

# Download process
print("Server has waiting for client to start download process\n")
download_file(download_client_socket)

# Close the connections
upload_client_socket.close()
download_client_socket.close()
upload_socket.close()
download_socket.close()