import sys
import os
import zlib
import hashlib
import struct

def read_git_object(obj_sha):
    """Read and decompress a git object"""
    obj_dir = obj_sha[:2]
    obj_file = obj_sha[2:]
    obj_path = os.path.join(".git", "objects", obj_dir, obj_file)
    
    with open(obj_path, "rb") as f:
        compressed_data = f.read()
    return zlib.decompress(compressed_data)

def parse_tree(tree_data):
    """Parse a tree object's content and return its entries"""
    entries = []
    i = 0
    
    # Skip the header (find null byte)
    null_pos = tree_data.find(b'\0')
    if null_pos == -1:
        raise RuntimeError("Invalid tree object: no null byte found")
    
    # Start parsing entries after the header
    i = null_pos + 1
    
    while i < len(tree_data):
        # Find the space that separates mode from name
        space_pos = tree_data.find(b' ', i)
        if space_pos == -1:
            break
            
        # Extract mode
        mode = tree_data[i:space_pos].decode('ascii')
        
        # Find null byte that separates name from SHA
        null_pos = tree_data.find(b'\0', space_pos + 1)
        if null_pos == -1:
            break
            
        # Extract name
        name = tree_data[space_pos + 1:null_pos].decode('utf-8')
        
        # Extract SHA (20 bytes)
        sha = tree_data[null_pos + 1:null_pos + 21].hex()
        
        # Determine type based on mode
        obj_type = "tree" if mode == "40000" else "blob"
        
        entries.append({
            'mode': mode,
            'type': obj_type,
            'sha': sha,
            'name': name
        })
        
        # Move to next entry
        i = null_pos + 21
    
    # Sort entries by name
    entries.sort(key=lambda x: x['name'])
    return entries

def ls_tree(tree_sha, name_only=False):
    """List the contents of a tree object"""
    try:
        tree_data = read_git_object(tree_sha)
        entries = parse_tree(tree_data)
        
        if name_only:
            # Print only the names
            for entry in entries:
                print(entry['name'])
        else:
            # Print full format
            for entry in entries:
                # Format mode to ensure 6 digits with leading zeros
                mode = entry['mode'].zfill(6)
                print(f"{mode} {entry['type']} {entry['sha']}\t{entry['name']}")
                
    except FileNotFoundError:
        raise RuntimeError(f"Not a valid object name {tree_sha}")
    
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
    if len(sys.argv) < 2:
        raise RuntimeError("Missing command")
        
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
        
        if len(sys.argv) < 3:
            raise RuntimeError("Missing file path")
        
        if sys.argv[2] == "-w":
            write_flag = True
            if len(sys.argv) < 4:
                raise RuntimeError("Missing file path")
            file_path = sys.argv[3]
        else:
            file_path = sys.argv[2]
        
        sha1 = hash_object(file_path, write_flag)
        print(sha1)
        
    elif command == "ls-tree":
        name_only = False
        tree_sha = ""
        
        if len(sys.argv) < 3:
            raise RuntimeError("Missing tree SHA")
            
        if sys.argv[2] == "--name-only":
            name_only = True
            if len(sys.argv) < 4:
                raise RuntimeError("Missing tree SHA")
            tree_sha = sys.argv[3]
        else:
            tree_sha = sys.argv[2]
            
        ls_tree(tree_sha, name_only)
        
    else:
        raise RuntimeError(f"Unknown command {command}")

if __name__ == "__main__":
    main()