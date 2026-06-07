---
scanner: no_os_command_injection_scanner.py
category: if
---

# Rule: No OS command injection

When code must invoke operating-system programs, pass arguments as an array without a shell intermediary. Building shell commands from user input enables metacharacter injection (`;`, `|`, `` ` ``, `$()`) — CWE-78, CWE-88, OWASP A03.

## DO

- **DO** use subprocess / spawn with an argument array and `shell=False` (default in Python 3).

  **Example (pass):**

  ```python
  subprocess.run(["convert", input_path, output_path], check=True)
  ```

  **Example (pass):**

  ```javascript
  const { spawn } = require('child_process');
  spawn('ffmpeg', ['-i', inputPath, outputPath]);
  ```

  **Example (pass):**

  ```java
  new ProcessBuilder("convert", inputPath, outputPath).start();
  ```

- **DO** validate and allow-list any value that still must influence command selection (host, format enum).

  **Example (pass):** Map `format=pdf` to internal enum before choosing converter binary — never pass raw user string as executable name.

- **DO** run with least privilege; log command invocations without secrets.

  **Example (pass):** Dedicated service account without shell login; audit log records argv array.

## DO NOT

- **DO NOT** pass user input into `shell=True` subprocess calls or shell-wrapped exec.

  **Example (fail):**

  ```python
  subprocess.run(f"grep {user_term} /var/log/app.log", shell=True)
  ```

- **DO NOT** concatenate untrusted strings into `os.system`, `child_process.exec`, or `Runtime.exec`.

  **Example (fail):**

  ```javascript
  exec('ffmpeg -i ' + req.query.file);
  ```

  **Example (fail):**

  ```java
  Runtime.getRuntime().exec("ping " + userIp);
  ```

- **DO NOT** rely on character blacklists to "sanitize" shell arguments — use structured argv or avoid shell entirely.

  **Example (fail):** Stripping `;` and `|` then passing remainder to `bash -c`.

**Source:** `context/05-injection-flaws/context/os-command-injection.md`, `context/05-injection-flaws/exercises-challenges/os-command-injection.md`
