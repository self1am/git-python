import sys
import os
import zlib

def read_blob(blob_sha):
    # Construct path to blob object
    obj_dir = blob_sha[:2]
    obj_file = blob_sha[2:]
    obj_path = os.path.join(".git", "objects", obj_dir, obj_file)
    
    # Read and decompress object
    with open(obj_path, "rb") as f:
        compressed_data = f.read()
    decompressed_data = zlib.decompress(compressed_data)
    
    # Parse the object header
    # Format is: "blob <size>\0<content>"
    header_end = decompressed_data.find(b'\0')
    header = decompressed_data[:header_end].decode('utf-8')
    
    # Verify this is a blob
    header_parts = header.split()
    if header_parts[0] != "blob":
        raise RuntimeError(f"Not a blob object: {header_parts[0]}")
    
    # Extract and return content
    content = decompressed_data[header_end + 1:]
    return content

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
        # Check if we have the correct number of arguments
        if len(sys.argv) != 4:
            raise RuntimeError("Missing blob SHA argument")
            
        blob_sha = sys.argv[3]
        content = read_blob(blob_sha)
        # Write content to stdout
        sys.stdout.buffer.write(content)
        
    else:
        raise RuntimeError(f"Unknown command {command}")

if __name__ == "__main__":
    main()