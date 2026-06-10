---
scanner: no_path_traversal_in_paths_scanner.py
category: id
---

# Rule: No path traversal in paths

When user input influences filesystem paths, validate and normalize before open/read/write. Traversal sequences (`../`) and absolute paths let attackers read or overwrite files outside the intended directory (CWE-22).

## DO

- **DO** resolve paths under a fixed base directory and reject if the result escapes the base.

  **Example (pass):**

  ```python
  base = UPLOAD_ROOT.resolve()
  target = (base / safe_filename).resolve()
  if not str(target).startswith(str(base)):
      raise PathTraversalError("invalid path")
  ```

  **Example (pass):**

  ```javascript
  const base = path.resolve(UPLOAD_DIR);
  const target = path.resolve(base, safeName);
  if (!target.startsWith(base + path.sep)) {
    throw new Error('path traversal');
  }
  ```

  **Example (pass):**

  ```java
  Path base = uploadRoot.toRealPath();
  Path target = base.resolve(safeName).normalize();
  if (!target.startsWith(base)) {
      throw new SecurityException("path traversal");
  }
  ```

- **DO** reject filenames containing path separators or `..` before mapping to storage keys.

  **Example (pass):** Allow-list `[a-zA-Z0-9._-]+` for user-visible download ids; map to internal UUID.

## DO NOT

- **DO NOT** concatenate request parameters into filesystem paths without normalization.

  **Example (fail):**

  ```python
  open(os.path.join("/data/reports", request.args["name"]))
  ```

- **DO NOT** pass raw `getParameter` / `req.params` values to `File`, `Paths.get`, or `fs.readFile`.

  **Example (fail):**

  ```java
  new File("/uploads/" + request.getParameter("file"));
  ```

- **DO NOT** decode `%2e%2e%2f` once and skip further validation — normalize and compare to base.

  **Example (fail):**

  ```javascript
  fs.readFileSync(path.join(STORAGE, req.query.path));
  ```

**Source:** `context/06-Insecure-Design/context/unrestricted-file-upload.md`, `context/05-injection-flaws/context/unrestricted-file-upload.md`
