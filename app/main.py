import sys
import os
import zlib
import hashlib

def read_blob(blob_sha):
    # Previous read_blob implementation remains the same
    obj_dir = blob_sha[:2]
    obj_file = blob_sha[2:]
    obj_path = os.path.join(".git", "objects", obj_dir, obj_file)
    
    with open(obj_path, "rb") as f:
        compressed_data = f.read()
    decompressed_data = zlib.decompress(compressed_data)
    
    header_end = decompressed_data.find(b'\0')
    header = decompressed_data[:header_end].decode('utf-8')
    
    header_parts = header.split()
    if header_parts[0] != "blob":
        raise RuntimeError(f"Not a blob object: {header_parts[0]}")
    
    content = decompressed_data[header_end + 1:]
    return content

def hash_object(file_path, write=False):
    # Read the content of the file
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Create the blob header
    header = f"blob {len(content)}".encode()
    store_data = header + b'\0' + content
    
    # Calculate SHA-1 hash
    sha1 = hashlib.sha1(store_data).hexdigest()
    
    if write:
        # Create object directory if it doesn't exist
        obj_dir = os.path.join(".git", "objects", sha1[:2])
        if not os.path.exists(obj_dir):
            os.makedirs(obj_dir)
            
        # Write compressed object
        obj_path = os.path.join(obj_dir, sha1[2:])
        compressed_data = zlib.compress(store_data)
        with open(obj_path, 'wb') as f:
            f.write(compressed_data)
    
    return sha1

def main():
    command = sys.argv[1]
    
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
        
    elif command == "cat-file" and sys.argv[2] == "-p":
        if len(sys.argv) != 4:
            raise RuntimeError("Missing blob SHA argument")
        blob_sha = sys.argv[3]
        content = read_blob(blob_sha)
        sys.stdout.buffer.write(content)
        
    elif command == "hash-object":
        write_flag = False
        file_path = ""
        
        # Parse arguments
        if len(sys.argv) < 3:
            raise RuntimeError("Missing file path")
        
        if sys.argv[2] == "-w":
            write_flag = True
            if len(sys.argv) < 4:
                raise RuntimeError("Missing file path")
            file_path = sys.argv[3]
        else:
            file_path = sys.argv[2]
        
        # Compute hash and optionally write object
        sha1 = hash_object(file_path, write_flag)
        print(sha1)
        
    else:
        raise RuntimeError(f"Unknown command {command}")

if __name__ == "__main__":
    main()