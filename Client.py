import socket

# Client configuration
SERVER_HOST = "127.0.0.1"
UPLOAD_PORT = 12345
DOWNLOAD_PORT = 12346
BUFFER_SIZE = 1024

def show_menu():
    print("\n1. Create a text file")
    print("2. Upload the file to the server")
    print("3. Download the file from the server")
    print("4. Compare files")
    print("5. Exit")
    choice = input("Enter your choice (1-4): ")
    return choice

def menu_upload():
    print("\n1. Use created file")
    print("2. Select another file")
    choice = input("Enter your choice (1-2): ")
    return choice

def upload_file(client_socket, cfile):
    
    choice = menu_upload()
    
    if choice == "1":
        if cfile.name != "0.fail":
            file_name = cfile.name
            with open(file_name, "rb") as file:
                file_data = file.read()
        else:
            print("Please create a file!")
            return cfile
    elif choice == "2":
        file_name = input("Enter the path of the file to upload: ")
        with open(file_name, "rb") as file:
            file_data = file.read()
    
    #Created file will be sent to the server
    client_socket.sendall(file_data)
    print(f"\nFile '{file_name}' sent to the server\n")
    
    return file

def download_file(client_socket):
    file_name = "student_info.txt"
    
    #File name is sending to the server
    client_socket.sendall(file_name.encode())
    
    #Server sends the requested file to the client
    file_data = client_socket.recv(BUFFER_SIZE)
    with open(file_name, "wb") as file:
        file.write(file_data)
    print(f"\nFile '{file_name}' downloaded from the server\n")
    return file

def create_file():
    file_name = input("Enter the name of the text file: ")
    content = input("Enter the content of the text file: ")
    with open(file_name, "w") as file:
        file.write(content)
    print(f"\nFile '{file_name}' created.\n")
    return file

def compare(ufile, dfile):
    with open(ufile.name) as file_1:
        file_1_text = file_1.read()
 
    with open(dfile.name) as file_2:
        file_2_text = file_2.read()
        
    if file_1_text==file_2_text:
        print("\nThe files are same.\n")
    else:
        print("\nThe files are not same.\n")
    
    

def main():
    
    file = open('0.fail', 'w')
    
    # Create sockets for upload and download
    upload_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server for upload and download
    upload_socket.connect((SERVER_HOST, UPLOAD_PORT))
    download_socket.connect((SERVER_HOST, DOWNLOAD_PORT))

    print(f"Connected for file upload to {SERVER_HOST}:{UPLOAD_PORT}")
    print(f"Connected for file download to {SERVER_HOST}:{DOWNLOAD_PORT}\n")

    while True:
        choice = show_menu()

        if choice == "1":
            file = create_file()
        elif choice == "2":
            ufile = upload_file(upload_socket, file)
        elif choice == "3":
            dfile = download_file(download_socket)
        elif choice == "4":
            compare(ufile, dfile)
        elif choice == "5":
            print("Exiting")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    # Close the connections
    upload_socket.close()
    download_socket.close()

if __name__ == "__main__":
    main()
