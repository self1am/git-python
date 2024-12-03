# Minimal Git Implementation

This Python program implements basic Git functionalities to explore Git objects, trees, and repositories. It provides commands for initializing a Git directory, listing tree contents, hashing objects, and more.

---

## Features

- **Initialize a Git Repository**: Set up a minimal `.git` directory structure.
- **Hash a File**: Compute and optionally write the hash of a file in Git's object storage.
- **Inspect Git Objects**: Read and display the content of a blob or tree object.
- **List Tree Contents**: Show the entries in a tree object.

---

## Commands and Usage

### 1. **Initialize a Repository**
   ```bash
   python script.py init
   ```
   Creates a minimal `.git` directory structure:
   - `.git/objects`
   - `.git/refs`
   - `.git/HEAD` pointing to `refs/heads/main`.

### 2. **Hash a File**
   ```bash
   python script.py hash-object [-w] <file_path>
   ```
   - Compute the SHA-1 hash of the file's content.
   - Optionally write the file into the `.git/objects` directory with the `-w` flag.

   **Examples**:
   - Compute hash only:
     ```bash
     python script.py hash-object file.txt
     ```
   - Compute hash and write:
     ```bash
     python script.py hash-object -w file.txt
     ```

### 3. **Inspect an Object**
   ```bash
   python script.py cat-file -p <object_sha>
   ```
   - Display the content of a Git object (blob, tree, etc.).
   - The object is identified by its SHA.

### 4. **List Tree Contents**
   ```bash
   python script.py ls-tree [--name-only] <tree_sha>
   ```
   - List the contents of a tree object.
   - The `--name-only` flag lists only entry names without additional details.

   **Examples**:
   - Full details:
     ```bash
     python script.py ls-tree <tree_sha>
     ```
   - Names only:
     ```bash
     python script.py ls-tree --name-only <tree_sha>
     ```

---

## Requirements

- Python 3.x

---

## Notes

- The program assumes a Git-like `.git` directory structure for file-based operations.
- Make sure you have a valid `.git` directory in the working directory for commands that interact with objects.

---

## Limitations

This implementation is a simplified version of Git and supports only core features:
- It does not handle branches, commits, or advanced Git concepts.
- The program operates on objects and trees manually, without the full Git plumbing.

---

## License

This project is open-source and available for educational purposes. Modify and adapt as needed!

---

## Author

Created by [Hanafe Mira].