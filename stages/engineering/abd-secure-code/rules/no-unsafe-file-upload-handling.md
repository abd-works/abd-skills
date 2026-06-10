---
scanner: no_unsafe_file_upload_handling_scanner.py
category: id
---

# Rule: No unsafe file upload handling

File uploads are a common path to remote code execution, path traversal, and denial of service. Production code must validate size, content type (magic bytes), and storage location — never trust client filenames, extensions, or `Content-Type` headers alone.

## DO

- **DO** generate internal storage names (UUID) and map to metadata in the database.

  **Example (pass):**

  ```python
  detected = magic.from_buffer(data, mime=True)
  if detected not in ALLOWED_MIME:
      raise InvalidUploadError("file type not allowed")
  safe_name = f"{uuid4().hex}.{ALLOWED_EXT[detected]}"
  storage.put(user_id, safe_name, data)
  ```

  **Example (pass):**

  ```java
  String safeName = UUID.randomUUID() + "." + validatedExtension;
  Path target = uploadRoot.resolve(safeName); // flat directory, no user segments
  Files.copy(inputStream, target, StandardCopyOption.REPLACE_EXISTING);
  ```

- **DO** enforce per-file and per-account size limits before reading the full stream.

  **Example (pass):** Reject when `Content-Length` or streamed byte count exceeds `MAX_UPLOAD_BYTES`.

- **DO** scan uploads in an isolated worker; serve from a separate domain or signed URLs when possible.

  **Example (pass):** Enqueue virus scan job; block download until scan status is `clean`.

## DO NOT

- **DO NOT** persist uploads using the client-provided original filename or extension alone.

  **Example (fail):**

  ```javascript
  cb(null, file.originalname);
  ```

- **DO NOT** allow uploads into web-root or executable directories.

  **Example (fail):**

  ```python
  save_path = os.path.join("/var/www/html/uploads", request.files["doc"].filename)
  ```

- **DO NOT** trust `Content-Type` or file extension without server-side magic-byte detection.

  **Example (fail):**

  ```javascript
  if (file.mimetype === 'image/png') { store(file); }
  ```

**Source:** `context/06-Insecure-Design/context/unrestricted-file-upload.md`, `context/06-Insecure-Design/exercises-challenges/File-Upload-Vulnerability-Unrestricted-File-Upload.md`
