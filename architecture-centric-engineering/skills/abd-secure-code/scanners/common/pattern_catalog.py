"""Central pattern catalog for abd-secure-code scanners (enterprise coverage).

Each entry: (compiled_regex, message, languages_tuple)
Languages: 'python', 'java', 'javascript', or 'all'
"""
from __future__ import annotations

import re
from typing import Literal

Language = Literal["python", "java", "javascript"]
PatternEntry = tuple[re.Pattern[str], str, tuple[str, ...]]

# ---------------------------------------------------------------------------
# no-hardcoded-secrets
# ---------------------------------------------------------------------------
_HARDCODED_SECRETS: list[PatternEntry] = [
    (
        re.compile(
            r"""(?i)(password|passwd|secret|api[_-]?key|private[_-]?key|access[_-]?token|client[_-]?secret|auth[_-]?token)\s*[:=]\s*['"][^'"\s]{8,}['"]"""
        ),
        "Hardcoded credential or secret literal in assignment.",
        ("all",),
    ),
    (
        re.compile(r"""AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}"""),
        "Possible AWS access key id embedded in source.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)(sk_live_|sk_test_|rk_live_|rk_test_)[a-zA-Z0-9]{16,}"""),
        "Possible Stripe secret key embedded in source.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)(xox[baprs]-|ghp_|gho_|ghu_|ghs_|ghr_)[a-zA-Z0-9_-]{10,}"""),
        "Possible Slack or GitHub token embedded in source.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"""),
        "Private key PEM block embedded in source file.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)(mongodb(\+srv)?|postgres(ql)?|mysql|redis)://[^'"\s]+:[^@/'"\s]+@"""),
        "Database connection string with embedded password in source.",
        ("all",),
    ),
    (
        re.compile(r"""['"]eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+['"]"""),
        "Hardcoded JWT string in source — use environment or secret manager.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)Basic\s+[A-Za-z0-9+/=]{20,}"""),
        "Hardcoded HTTP Basic credentials in source.",
        ("all",),
    ),
]

# ---------------------------------------------------------------------------
# no-sql-string-concatenation (regex supplement; Python also uses AST)
# ---------------------------------------------------------------------------
_SQL_CONCAT: list[PatternEntry] = [
    (
        re.compile(
            r"""['"][^'"]*\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE)\b[^'"]*['"]\s*(\+|\.format|String\.format)"""
        ),
        "SQL statement built via concatenation or format — use bound parameters.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)(execute|executemany|query|raw)\s*\(\s*f['"]"""),
        "Dynamic f-string passed to SQL execute/query API.",
        ("python",),
    ),
    (
        re.compile(r"""(?i)\.query\s*\(\s*`[^`]*\$\{"""),
        "Template literal SQL with interpolation passed to query().",
        ("javascript",),
    ),
    (
        re.compile(r"""(?i)(knex\.raw|sequelize\.query)\s*\(\s*`"""),
        "ORM raw SQL with template literal — verify parameters are bound.",
        ("javascript",),
    ),
    (
        re.compile(
            r"""createStatement\s*\(\s*\)\.execute(Query|Update|)\s*\(\s*["'][^"']*\+"""
        ),
        "JDBC Statement with concatenated SQL — use PreparedStatement.",
        ("java",),
    ),
    (
        re.compile(r"""executeQuery\s*\([^)]*\+"""),
        "executeQuery with string concatenation — use PreparedStatement placeholders.",
        ("java",),
    ),
    (
        re.compile(r"""executeUpdate\s*\([^)]*\+"""),
        "executeUpdate with string concatenation — use PreparedStatement placeholders.",
        ("java",),
    ),
]

# ---------------------------------------------------------------------------
# no-os-command-injection
# ---------------------------------------------------------------------------
_OS_COMMAND: list[PatternEntry] = [
    (
        re.compile(r"""subprocess\.(call|run|Popen|check_output|check_call)\([^)]*shell\s*=\s*True"""),
        "subprocess with shell=True allows shell metacharacter injection.",
        ("python",),
    ),
    (
        re.compile(r"""\bos\.system\s*\("""),
        "os.system executes through a shell — use subprocess with argument list.",
        ("python",),
    ),
    (
        re.compile(r"""\bos\.popen\s*\("""),
        "os.popen executes through a shell.",
        ("python",),
    ),
    (
        re.compile(r"""subprocess\.(call|run|Popen)\([^)]*f['"]"""),
        "Shell command built via f-string before subprocess invocation.",
        ("python",),
    ),
    (
        re.compile(r"""(?i)child_process\.(exec|execSync)\s*\(\s*['"`][^'"`]*\+"""),
        "child_process.exec with concatenated command string.",
        ("javascript",),
    ),
    (
        re.compile(r"""(?i)child_process\.(exec|execSync)\s*\(\s*`"""),
        "child_process.exec with template literal command — prefer spawn with args array.",
        ("javascript",),
    ),
    (
        re.compile(r"""(?i)spawn\s*\([^,]+,\s*[^,]+,\s*\{[^}]*shell\s*:\s*true"""),
        "spawn with shell:true and user-influenced arguments risks injection.",
        ("javascript",),
    ),
    (
        re.compile(r"""Runtime\.getRuntime\s*\(\s*\)\.exec\s*\([^)]*\+"""),
        "Runtime.exec with concatenated command string.",
        ("java",),
    ),
    (
        re.compile(r"""new ProcessBuilder\s*\([^)]*\+"""),
        "ProcessBuilder command built via string concatenation.",
        ("java",),
    ),
]

# ---------------------------------------------------------------------------
# no-eval-dynamic-code-execution
# ---------------------------------------------------------------------------
_EVAL: list[PatternEntry] = [
    (re.compile(r"""\beval\s*\("""), "eval executes arbitrary code — never on untrusted input.", ("python", "javascript")),
    (re.compile(r"""\bexec\s*\("""), "exec executes arbitrary code — never on untrusted input.", ("python",)),
    (re.compile(r"""\bcompile\s*\([^)]*['"]exec['"]"""), "compile(..., 'exec') enables dynamic code execution.", ("python",)),
    (re.compile(r"""\bnew\s+Function\s*\("""), "Function constructor executes arbitrary code from strings.", ("javascript",)),
    (re.compile(r"""setTimeout\s*\(\s*['"]"""), "setTimeout with string argument is equivalent to eval.", ("javascript",)),
    (re.compile(r"""setInterval\s*\(\s*['"]"""), "setInterval with string argument is equivalent to eval.", ("javascript",)),
    (re.compile(r"""vm\.runIn(NewContext|ThisContext)\s*\("""), "vm.runIn* executes code strings — sandbox carefully.", ("javascript",)),
    (re.compile(r"""ScriptEngine.*\.eval\s*\("""), "ScriptEngine.eval on external input enables script injection.", ("java",)),
    (re.compile(r"""NashornScriptEngine|javax\.script\.ScriptEngine"""), "Script engine on external input — verify strict allow-list.", ("java",)),
]

# ---------------------------------------------------------------------------
# no-dangerous-xss-sinks
# ---------------------------------------------------------------------------
_XSS: list[PatternEntry] = [
    (re.compile(r"""dangerouslySetInnerHTML"""), "dangerouslySetInnerHTML bypasses React escaping.", ("javascript",)),
    (re.compile(r"""\.innerHTML\s*="""), "innerHTML assignment with untrusted content enables XSS.", ("javascript",)),
    (re.compile(r"""\.outerHTML\s*="""), "outerHTML assignment with untrusted content enables XSS.", ("javascript",)),
    (re.compile(r"""document\.write\s*\("""), "document.write with untrusted content enables XSS.", ("javascript",)),
    (re.compile(r"""insertAdjacentHTML\s*\("""), "insertAdjacentHTML requires sanitization for untrusted HTML.", ("javascript",)),
    (re.compile(r"""bypassSecurityTrust(Html|Script|Url|ResourceUrl|Style)"""), "Angular trust bypass disables sanitization.", ("javascript",)),
    (re.compile(r"""v-html\s*="""), "Vue v-html renders raw HTML — sanitize untrusted content first.", ("javascript",)),
    (re.compile(r"""(?i)\|\s*safe\b"""), "Jinja '|safe' filter disables auto-escaping.", ("python",)),
    (re.compile(r"""(?i)Markup\s*\([^)]*request\."""), "Markup() wrapping request content bypasses escaping.", ("python",)),
    (re.compile(r"""(?i)autoescape\s*=\s*False"""), "Disabling template autoescape increases XSS risk.", ("python",)),
    (re.compile(r"""response\.getWriter\s*\(\s*\)\.(print|write)\s*\(\s*request\.getParameter"""), "Writing raw request parameter to response without encoding.", ("java",)),
    (re.compile(r"""<%=\s*request\.getParameter"""), "JSP expression of request parameter without encoding.", ("java",)),
]

# ---------------------------------------------------------------------------
# no-plaintext-password-storage
# ---------------------------------------------------------------------------
_PLAINTEXT_PASSWORD: list[PatternEntry] = [
    (
        re.compile(r"""(?i)(save|insert|update|create|persist|store).{0,40}password\s*[:=]\s*(req\.|request\.|body\.|params\.|getParameter)"""),
        "Password from request persisted without adaptive hashing.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)setPassword\s*\(\s*(req\.|request\.|plain|raw|password\b)"""),
        "setPassword called with plaintext or request-derived value.",
        ("java", "javascript"),
    ),
    (
        re.compile(r"""(?i)User\.(create|update|insert)\([^)]*password\s*:\s*req\."""),
        "ORM create/update with plaintext password field from request.",
        ("javascript",),
    ),
    (
        re.compile(r"""(?i)logger\.(info|debug|warn|error).{0,30}password"""),
        "Logging password values during authentication flow.",
        ("all",),
    ),
]

# ---------------------------------------------------------------------------
# no-sensitive-error-disclosure
# ---------------------------------------------------------------------------
_ERROR_DISCLOSURE: list[PatternEntry] = [
    (re.compile(r"""(?i)traceback\.format_exc\s*\("""), "Full traceback may leak paths and versions.", ("python",)),
    (re.compile(r"""(?i)(return|send|jsonify|Response)\([^)]*traceback"""), "Returning traceback in HTTP response.", ("python",)),
    (re.compile(r"""(?i)(return|send|jsonify|Response)\([^)]*format_exc"""), "Returning format_exc output to client.", ("python",)),
    (re.compile(r"""(?i)(return|send|jsonify)\([^)]*\.stack\b"""), "Returning err.stack exposes internals.", ("javascript", "python")),
    (re.compile(r"""['"]stack['"]\s*:"""), "Response body includes stack field.", ("all",)),
    (re.compile(r"""(?i)printStackTrace\s*\(\s*\)"""), "printStackTrace exposes stack trace.", ("java",)),
    (re.compile(r"""(?i)res\.(status\([^)]+\)\.)?send\s*\(\s*err\.stack"""), "Sending err.stack in HTTP response.", ("javascript",)),
    (re.compile(r"""(?i)ResponseEntity.*getStackTrace"""), "Stack trace returned in ResponseEntity.", ("java",)),
    (re.compile(r"""(?i)debug\s*=\s*True"""), "Debug mode enabled — disable in production.", ("python",)),
    (re.compile(r"""(?i)app\.set\s*\(\s*['"]env['"]\s*,\s*['"]development['"]"""), "Express env set to development in production code path.", ("javascript",)),
    (re.compile(r"""(?i)server\.error\.include-stacktrace\s*=\s*always"""), "Spring include-stacktrace=always leaks traces to clients.", ("java",)),
]

# ---------------------------------------------------------------------------
# no-unsafe-deserialization
# ---------------------------------------------------------------------------
_UNSAFE_DESER: list[PatternEntry] = [
    (re.compile(r"""\bpickle\.loads\s*\("""), "pickle.loads on untrusted input enables RCE.", ("python",)),
    (re.compile(r"""\bpickle\.load\s*\("""), "pickle.load on untrusted stream enables RCE.", ("python",)),
    (re.compile(r"""\byaml\.load\s*\("""), "yaml.load without SafeLoader can execute arbitrary objects.", ("python",)),
    (re.compile(r"""\bmarshal\.loads\s*\("""), "marshal.loads must never process untrusted bytes.", ("python",)),
    (re.compile(r"""\bshelve\.open\s*\("""), "shelve uses pickle internally — not for untrusted data.", ("python",)),
    (re.compile(r"""(?i)ObjectInputStream\s*\("""), "ObjectInputStream deserializes untrusted byte streams.", ("java",)),
    (re.compile(r"""(?i)\.readObject\s*\(\s*\)"""), "readObject() on untrusted serialized data.", ("java",)),
    (re.compile(r"""XMLDecoder\s*\("""), "XMLDecoder can instantiate arbitrary objects from XML.", ("java",)),
    (re.compile(r"""XStream.*fromXML"""), "XStream fromXML on external input without type allow-list.", ("java",)),
    (re.compile(r"""Yaml\.load\s*\("""), "SnakeYAML load without SafeConstructor on external input.", ("java",)),
    (re.compile(r"""(?i)node-serialize|serialize\.unserialize"""), "node-serialize can execute code during unserialize.", ("javascript",)),
    (re.compile(r"""(?i)eval\s*\(\s*JSON\.parse"""), "eval(JSON.parse(...)) executes parsed content as code.", ("javascript",)),
]

# ---------------------------------------------------------------------------
# no-mass-assignment-from-request
# ---------------------------------------------------------------------------
_MASS_ASSIGNMENT: list[PatternEntry] = [
    (re.compile(r"""(?i)\*\*request\.(json|form|data|args|values|GET|POST)"""), "Spreading entire request dict into model.", ("python",)),
    (re.compile(r"""(?i)\*\*(body|data|payload|form)\b"""), "Keyword-unpacking request dict into model constructor.", ("python",)),
    (re.compile(r"""(?i)\.update\s*\(\s*request\.(json|form|data)"""), "Bulk ORM update from unfiltered request.", ("python",)),
    (re.compile(r"""(?i)Object\.assign\s*\([^,]+,\s*req\.body"""), "Object.assign from req.body without allow-list.", ("javascript",)),
    (re.compile(r"""(?i)\{\s*\.\.\.req\.body"""), "Spreading req.body into entity without filtering.", ("javascript",)),
    (re.compile(r"""(?i)findByIdAndUpdate\s*\([^,]+,\s*req\.body"""), "Mongo findByIdAndUpdate with unfiltered body.", ("javascript",)),
    (re.compile(r"""(?i)\.update\s*\(\s*req\.body\s*\)"""), "ORM update with entire req.body payload.", ("javascript",)),
    (re.compile(r"""BeanUtils\.(copyProperties|populate)\s*\([^,]+,\s*request"""), "BeanUtils binding from request without allow-list.", ("java",)),
    (re.compile(r"""ObjectMapper.*convertValue\s*\(\s*request"""), "convertValue from raw request without DTO validation.", ("java",)),
]

# ---------------------------------------------------------------------------
# no-weak-crypto-algorithms
# ---------------------------------------------------------------------------
_WEAK_CRYPTO: list[PatternEntry] = [
    (re.compile(r"""(?i)hashlib\.(md5|sha1)\s*\("""), "MD5/SHA1 not suitable for password or integrity protection.", ("python",)),
    (re.compile(r"""(?i)DES\.|TripleDES|Algorithm\.DES"""), "DES/3DES are deprecated symmetric ciphers.", ("python", "java")),
    (re.compile(r"""(?i)modes\.ECB\b"""), "ECB mode lacks semantic security.", ("python",)),
    (re.compile(r"""(?i)createHash\s*\(\s*['"]md5['"]"""), "MD5 not suitable for security-sensitive hashing.", ("javascript",)),
    (re.compile(r"""(?i)createHash\s*\(\s*['"]sha1['"]"""), "SHA1 weak for security-sensitive hashing.", ("javascript",)),
    (re.compile(r"""(?i)createCipher\s*\("""), "Legacy createCipher — use createCipheriv with AEAD.", ("javascript",)),
    (re.compile(r"""MessageDigest\.getInstance\s*\(\s*["']MD5["']"""), "MD5 must not be used for password storage.", ("java",)),
    (re.compile(r"""MessageDigest\.getInstance\s*\(\s*["']SHA-?1["']"""), "SHA-1 must not be used for password storage.", ("java",)),
    (re.compile(r"""Cipher\.getInstance\s*\(\s*["']DES"""), "DES is a weak cipher.", ("java",)),
    (re.compile(r"""Cipher\.getInstance\s*\(\s*["']RC4"""), "RC4 is a weak cipher.", ("java",)),
    (re.compile(r"""Signature\.getInstance\s*\(\s*["']SHA1withRSA["']"""), "SHA1withRSA is deprecated for new code.", ("java",)),
    (re.compile(r"""setSigningKey\s*\(\s*["']"""), "Hardcoded JWT signing key in source.", ("java", "javascript")),
]

_WEAK_CRYPTO_CONTEXT: list[PatternEntry] = [
    (re.compile(r"""(?i)Math\.random\s*\("""), "Math.random is not CSPRNG — use crypto.randomBytes for tokens.", ("javascript",)),
    (re.compile(r"""(?i)random\.randint\s*\("""), "random.randint is not CSPRNG — use secrets module for tokens.", ("python",)),
    (re.compile(r"""\bRandom\s*\(\s*\)"""), "java.util.Random is not CSPRNG — use SecureRandom for tokens.", ("java",)),
]

# ---------------------------------------------------------------------------
# no-predictable-session-token (NEW)
# ---------------------------------------------------------------------------
_PREDICTABLE_SESSION: list[PatternEntry] = [
    (re.compile(r"""(?i)req\.session\.id\s*="""), "Session id assigned directly from request/session — use server-generated id.", ("javascript",)),
    (re.compile(r"""(?i)session[_-]?id\s*=\s*(username|user\.name|user_name|email)\b"""), "Session id derived from username — predictable.", ("all",)),
    (re.compile(r"""(?i)sessionId\s*=\s*(username|user\.name|user_name|email)\s*;"""), "Session id derived from username — predictable.", ("java",)),
    (re.compile(r"""(?i)session[_-]?id\s*=\s*(user[_-]?id|userId|user\.id)"""), "Session id derived from user id — predictable.", ("all",)),
    (re.compile(r"""(?i)sessionId\s*=\s*(user[_-]?id|userId|user\.id)"""), "Session id derived from user id — predictable.", ("java",)),
    (re.compile(r"""(?i)session[_-]?id\s*=\s*session[_-]?id\s*\+\s*1"""), "Incrementing session id is predictable.", ("all",)),
    (re.compile(r"""(?i)session[_-]?id\s*=\s*String\.valueOf\s*\(\s*random\.nextInt\s*\(\s*100000"""), "Small random range for session id is brute-forceable.", ("java",)),
    (re.compile(r"""(?i)session[_-]?id\s*=\s*Math\.floor\s*\(\s*Math\.random"""), "Math.random session id is predictable and low entropy.", ("javascript",)),
]

# ---------------------------------------------------------------------------
# no-unsafe-file-upload-handling (NEW)
# ---------------------------------------------------------------------------
_UNSAFE_UPLOAD: list[PatternEntry] = [
    (re.compile(r"""(?i)(save|store|write)\([^)]*originalFilename"""), "Storing upload using client-provided originalFilename.", ("java",)),
    (re.compile(r"""(?i)transferTo\s*\(\s*[^)]*getOriginalFilename"""), "transferTo path uses client original filename.", ("java",)),
    (re.compile(r"""(?i)multer\s*\(\s*\{[^}]*destination[^}]*\}\s*\)"""), "Verify multer uses generated filenames and type validation.", ("javascript",)),
    (re.compile(r"""(?i)filename\s*:\s*function\s*\([^)]*\)\s*\{[^}]*file\.originalname"""), "Multer filename callback uses originalname without sanitization.", ("javascript",)),
    (re.compile(r"""(?i)save\s*\(\s*[^)]*\.filename\b"""), "Saving upload using unsanitized .filename from request.", ("python", "javascript")),
    (
        re.compile(r"""(?i)(/uploads/|/var/www)[^'"]*\+[^'"]*\.filename"""),
        "Upload path built with client .filename.",
        ("python",),
    ),
    (
        re.compile(r"""(?i)\.filename\b"""),
        "Upload path or save uses client-provided .filename without sanitization.",
        ("python",),
    ),
    (
        re.compile(r"""(?i)originalname"""),
        "Upload handler references client originalname without UUID rename.",
        ("javascript",),
    ),
    (re.compile(r"""(?i)Content-Type['"]\s*:\s*file\.mimetype"""), "Trusting client Content-Type/mimetype alone for upload validation.", ("javascript",)),
    (re.compile(r"""(?i)allowed_extensions\s*=\s*\[\s*['"]\."""), "Extension-only allow-list without magic-byte validation.", ("python",)),
]

# ---------------------------------------------------------------------------
# no-path-traversal-in-paths (NEW)
# ---------------------------------------------------------------------------
_PATH_TRAVERSAL: list[PatternEntry] = [
    (re.compile(r"""(?i)(path\.join|os\.path\.join|Path\s*\([^)]*\/)\s*[^)]*(req\.|request\.|params\.|query\.|getParameter)"""), "Path join includes request-derived segment without normalization.", ("python", "javascript")),
    (re.compile(r"""(?i)open\s*\(\s*[^)]*\+[^)]*(request\.|req\.|args\[)"""), "File open with concatenated request-derived path.", ("python",)),
    (re.compile(r"""(?i)(readFile|writeFile|createReadStream|createWriteStream)\s*\([^)]*\+[^)]*req\."""), "fs operation with concatenated request path.", ("javascript",)),
    (re.compile(r"""(?i)path\.join\s*\([^)]*req\."""), "path.join includes request-derived segment without normalization.", ("javascript",)),
    (re.compile(r"""Paths\.get\s*\([^)]*getParameter[^)]*\)"""), "Paths.get with raw request parameter — validate and normalize.", ("java",)),
    (re.compile(r"""(?i)new\s+(\w+\.)*File\s*\([^)]*getParameter"""), "File constructor with raw request parameter.", ("java",)),
    (re.compile(r"""FileUtils\.(read|write).*getParameter"""), "FileUtils operation with raw request parameter.", ("java",)),
]

# ---------------------------------------------------------------------------
# no-secrets-in-log-output (NEW)
# ---------------------------------------------------------------------------
_SECRETS_IN_LOGS: list[PatternEntry] = [
    (re.compile(r"""(?i)(logger|log|logging)\.(info|debug|warn|error|exception)\([^)]*password"""), "Logging statement includes password field.", ("all",)),
    (re.compile(r"""(?i)console\.(log|info|debug|warn|error)\([^)]*password"""), "console.log includes password field.", ("javascript",)),
    (re.compile(r"""(?i)(logger|log)\.(info|debug|warn|error)\([^)]*secret"""), "Logging statement includes secret field.", ("all",)),
    (re.compile(r"""(?i)(logger|log)\.(info|debug|warn|error)\([^)]*api[_-]?key"""), "Logging statement includes api_key field.", ("all",)),
    (re.compile(r"""(?i)(logger|log)\.(info|debug|warn|error)\([^)]*authorization"""), "Logging Authorization header may capture bearer tokens.", ("all",)),
    (re.compile(r"""(?i)print\s*\([^)]*password"""), "print() includes password in output.", ("python",)),
    (re.compile(r"""(?i)\.info\s*\(\s*["'][^"']*password"""), "SLF4J log template references password.", ("java",)),
]

# ---------------------------------------------------------------------------
# LDAP filter injection (CWE-90)
# ---------------------------------------------------------------------------
_LDAP_FILTER: list[PatternEntry] = [
    (re.compile(r"""(?i)Ldap\.search\s*\([^)]*\(\s*(email|uid|cn)\s*=\s*\{0\}"""), "LDAP filter uses MessageFormat placeholder without escaping.", ("all",)),
    (re.compile(r"""(?i)\(\s*(email|uid|mail|cn)\s*=\s*["']\s*\+\s*"""), "LDAP filter built via string concatenation.", ("all",)),
    (re.compile(r"""(?i)ldapTemplate\.search\s*\(\s*["']\([^)]+\)\s*\+\s*"""), "Spring LDAP search filter concatenates user input.", ("java",)),
    (re.compile(r"""(?i)\.search\s*\([^,]+,\s*["']\([^)]+\)\s*\+\s*"""), "DirContext.search with concatenated filter.", ("java",)),
    (re.compile(r"""(?i)filter\s*=\s*f?["']\([^)]+\)\$\{"""), "LDAP filter template embeds untrusted value.", ("javascript",)),
    (re.compile(r"""(?i)conn\.search\s*\([^,]+,\s*f?["']\([^)]+\)\{"""), "ldap3 search filter embeds untrusted value.", ("python",)),
]

# ---------------------------------------------------------------------------
# XXE / unsafe XML parser (CWE-611)
# ---------------------------------------------------------------------------
_XXE_UNSAFE: list[PatternEntry] = [
    (re.compile(r"""DocumentBuilderFactory\.newInstance\(\)\.newDocumentBuilder\(\)\.parse"""), "DocumentBuilder parses without explicit XXE hardening.", ("java",)),
    (re.compile(r"""SAXParserFactory\.newInstance\(\)\.newSAXParser\(\)"""), "SAXParser created without disallow-doctype / external entities.", ("java",)),
    (re.compile(r"""XMLInputFactory\.newInstance\(\)"""), "XMLInputFactory may allow external entities by default.", ("java",)),
    (re.compile(r"""etree\.parse\s*\("""), "xml.etree parses untrusted XML without defusedxml.", ("python",)),
    (re.compile(r"""lxml\.etree\.parse\s*\("""), "lxml parses untrusted XML without hardening.", ("python",)),
    (re.compile(r"""DOMParser\s*\(\)\.parseFromString"""), "DOMParser may resolve external entities in some environments.", ("javascript",)),
]

# ---------------------------------------------------------------------------
# Untrusted component sources (CWE-829)
# ---------------------------------------------------------------------------
_UNTRUSTED_COMPONENTS: list[PatternEntry] = [
    (re.compile(r"""pip\s+install\s+https?://"""), "pip install from HTTP(S) URL — supply-chain risk.", ("all",)),
    (re.compile(r"""git\+https?://"""), "Dependency pinned to remote git URL without verification.", ("all",)),
    (re.compile(r"""npm\s+install\s+https?://"""), "npm install from arbitrary URL.", ("all",)),
    (re.compile(r"""require\s*\(\s*req\.(query|body|params)\."""), "Dynamic require from request — remote code load risk.", ("javascript",)),
    (re.compile(r"""eval\s*\(\s*await\s+fetch"""), "Eval of remotely fetched script.", ("javascript",)),
]

# ---------------------------------------------------------------------------
# Insufficient login rate limiting (CWE-307) — baseline patterns; see catalog_scanner
# ---------------------------------------------------------------------------
_LOGIN_NO_LIMIT: list[PatternEntry] = [
    (re.compile(r"""(?i)app\.post\s*\(\s*['"]/login['"]"""), "Express login POST without rate limiter in signature.", ("javascript",)),
    (re.compile(r"""(?i)PostMapping\s*\(\s*["']/login"""), "Spring login endpoint — verify rate limiting.", ("java",)),
    (re.compile(r"""(?i)def\s+login\s*\("""), "Login handler — verify rate limiting middleware.", ("python",)),
]

# ---------------------------------------------------------------------------
# TOCTOU outside lock (CWE-367)
# ---------------------------------------------------------------------------
_TOCTOU: list[PatternEntry] = [
    (re.compile(r"""getBalance\s*\(\s*\)\s*<\s*"""), "Balance check may occur outside critical section.", ("java",)),
    (re.compile(r"""\.balance\s*<\s*"""), "Balance comparison may occur outside lock.", ("python",)),
    (re.compile(r"""\.balance\s*<\s*"""), "Balance comparison may occur outside lock.", ("javascript",)),
]

# ---------------------------------------------------------------------------
# Missing security event logging (CWE-778)
# ---------------------------------------------------------------------------
_AUTH_HANDLER: list[PatternEntry] = [
    (re.compile(r"""(?i)app\.post\s*\(\s*['"]/login['"]"""), "Login handler — verify security events are logged.", ("javascript",)),
    (re.compile(r"""(?i)app\.post\s*\(\s*['"]/logout['"]"""), "Logout handler — verify security events are logged.", ("javascript",)),
    (re.compile(r"""(?i)PostMapping\s*\(\s*["']/(login|logout|authenticate)"""), "Auth endpoint — verify security events are logged.", ("java",)),
    (re.compile(r"""(?i)def\s+(login|logout|authenticate)\s*\("""), "Auth handler — verify security events are logged.", ("python",)),
]

# ---------------------------------------------------------------------------
# Excessive API response data (CWE-200)
# ---------------------------------------------------------------------------
_EXCESSIVE_RESPONSE: list[PatternEntry] = [
    (re.compile(r"""(?i)res\.json\s*\(\s*(user|patient|entity|profile|account)\s*\)"""), "Returning full domain entity in JSON response.", ("javascript",)),
    (re.compile(r"""(?i)res\.send\s*\(\s*(user|patient|entity|profile|account)\s*\)"""), "Sending full domain entity in HTTP response.", ("javascript",)),
    (re.compile(r"""(?i)return\s+jsonify\s*\(\s*(user|patient|entity|profile|account)\b"""), "jsonify returns full entity without DTO mapping.", ("python",)),
    (re.compile(r"""(?i)return\s+jsonify\s*\(\s*(user|patient)\.__dict__"""), "Serializing ORM __dict__ exposes all fields.", ("python",)),
    (re.compile(r"""(?i)JsonResponse\s*\(\s*(user|patient|entity)\.to_dict\s*\("""), "to_dict() may expose internal ORM fields.", ("python",)),
    (re.compile(r"""(?:[\w.]+\.)?ResponseEntity\.ok\s*\(\s*(user|patient|entity|account)Repository\.find"""), "Returning raw repository entity in ResponseEntity.", ("java",)),
    (re.compile(r"""(?:[\w.]+\.)?ResponseEntity\.ok\s*\(\s*(user|patient|entity|account)\s*\)"""), "Returning full entity in ResponseEntity.", ("java",)),
    (re.compile(r"""return\s+(user|patient|entity|account)\s*;"""), "Returning full entity — use a response DTO.", ("java",)),
]

# ---------------------------------------------------------------------------
# Plaintext sensitive data at rest (CWE-312)
# ---------------------------------------------------------------------------
_PLAINTEXT_SENSITIVE: list[PatternEntry] = [
    (
        re.compile(
            r"""(?i)(save|insert|update|create|persist|store).{0,50}(ssn|social_security|tax_id|credit_card|card_number|national_id|passport|bank_account)\s*[:=]\s*(req\.|request\.|body\.|params\.|getParameter)"""
        ),
        "Sensitive PII from request persisted without encryption.",
        ("all",),
    ),
    (
        re.compile(r"""(?i)set(Ssn|SocialSecurity|TaxId|CreditCard|NationalId|Passport)\s*\(\s*(req\.|request\.|plain|raw)"""),
        "Setter called with plaintext sensitive field from request.",
        ("java",),
    ),
    (
        re.compile(r"""(?i)\.(create|insert|update)\([^)]*(ssn|social_security|tax_id|credit_card)\s*:\s*req\."""),
        "ORM write with plaintext sensitive field from request.",
        ("javascript",),
    ),
    (
        re.compile(r"""(?i)INSERT\s+INTO\s+\w+\s*\([^)]*(ssn|social_security|tax_id|credit_card)"""),
        "SQL insert names sensitive column — verify encryption at rest.",
        ("all",),
    ),
]

# ---------------------------------------------------------------------------
# Client-side auth trust (CWE-287)
# ---------------------------------------------------------------------------
_CLIENT_AUTH_TRUST: list[PatternEntry] = [
    (re.compile(r"""(?i)Buffer\.from\s*\(\s*JSON\.stringify"""), "Base64 JSON cookie auth — use server-side session or signed token.", ("javascript",)),
    (re.compile(r"""(?i)JSON\.parse\s*\(\s*Buffer\.from\s*\([^)]*base64"""), "Parsing base64 cookie JSON as authentication state.", ("javascript",)),
    (re.compile(r"""(?i)JSON\.parse\s*\(\s*atob\s*\("""), "atob cookie parsed as session — not integrity protected.", ("javascript",)),
    (re.compile(r"""(?i)atob\s*\(\s*req\.cookies"""), "Decoding cookie with atob for auth decisions.", ("javascript",)),
    (re.compile(r"""(?i)res\.cookie\s*\([^)]*Buffer\.from\s*\(\s*JSON\.stringify"""), "Setting unsigned base64 user object in cookie.", ("javascript",)),
    (re.compile(r"""Base64\.getDecoder\(\)\.decode\s*\([^)]*[Cc]ookie"""), "Base64-decoding cookie value for auth state.", ("java",)),
    (re.compile(r"""Base64\.getEncoder\(\)\.encodeToString"""), "Base64-encoding object into cookie — not integrity protected.", ("java",)),
    (re.compile(r"""addCookie\s*\(\s*new\s+javax\.servlet\.http\.Cookie\s*\(\s*["']user["']"""), "Unsigned user cookie set from serialized object.", ("java",)),
    (re.compile(r"""(?i)btoa\s*\(\s*JSON\.stringify\s*\(\s*\{[^}]*(role|isAdmin)"""), "Encoding role/admin JSON into client cookie.", ("javascript",)),
    (re.compile(r"""(?i)base64\.b64encode\s*\(\s*json\.dumps"""), "Base64 JSON cookie auth — use server-side session or signed token.", ("python",)),
    (re.compile(r"""(?i)set_cookie\s*\(\s*["']user["']"""), "Unsigned user object stored in client cookie.", ("python",)),
]

# ---------------------------------------------------------------------------
# JWT none / missing verification (CWE-347)
# ---------------------------------------------------------------------------
_JWT_NONE: list[PatternEntry] = [
    (re.compile(r"""(?i)jwt\.verify\s*\([^)]*algorithms\s*:\s*\[[^\]]*['"]none['"]"""), "jwt.verify allows algorithm none.", ("javascript",)),
    (re.compile(r"""(?i)jwt\.verify\s*\(\s*[^,]+,\s*null\s*,"""), "jwt.verify with null secret — often paired with alg none.", ("javascript",)),
    (re.compile(r"""(?i)jwt\.sign\s*\([^)]*algorithm\s*:\s*['"]none['"]"""), "JWT signed with algorithm none.", ("javascript",)),
    (re.compile(r"""(?i)algorithm\s*=\s*['"]none['"]"""), "JWT algorithm none disables signature verification.", ("python", "javascript")),
    (re.compile(r"""["']alg["']\s*:\s*["']none["']"""), "JWT header alg none disables signature verification.", ("javascript", "python")),
    (re.compile(r"""(?i)jwt\.decode\s*\([^)]*verify_signature["\']?\s*:\s*False"""), "JWT decoded without signature verification.", ("python",)),
    (re.compile(r"""(?i)options\s*=\s*\{[^}]*verify_signature["\']?\s*:\s*False"""), "JWT decode skips signature verification.", ("python", "javascript")),
    (re.compile(r"""Jwts\.parserBuilder\(\)\.setSigningKey\s*\(\s*null\s*\)"""), "JJWT parser with null signing key.", ("java",)),
    (re.compile(r"""parseClaimsJwt\s*\("""), "parseClaimsJwt accepts unsigned JWT — use parseClaimsJws.", ("java",)),
]

# ---------------------------------------------------------------------------
# Catalog registry
# ---------------------------------------------------------------------------
CATALOG: dict[str, list[PatternEntry]] = {
    "no-hardcoded-secrets": _HARDCODED_SECRETS,
    "no-sql-string-concatenation": _SQL_CONCAT,
    "no-os-command-injection": _OS_COMMAND,
    "no-eval-dynamic-code-execution": _EVAL,
    "no-dangerous-xss-sinks": _XSS,
    "no-plaintext-password-storage": _PLAINTEXT_PASSWORD,
    "no-sensitive-error-disclosure": _ERROR_DISCLOSURE,
    "no-unsafe-deserialization": _UNSAFE_DESER,
    "no-mass-assignment-from-request": _MASS_ASSIGNMENT,
    "no-weak-crypto-algorithms": _WEAK_CRYPTO,
    "no-predictable-session-token": _PREDICTABLE_SESSION,
    "no-unsafe-file-upload-handling": _UNSAFE_UPLOAD,
    "no-path-traversal-in-paths": _PATH_TRAVERSAL,
    "no-secrets-in-log-output": _SECRETS_IN_LOGS,
    "no-ldap-filter-injection": _LDAP_FILTER,
    "no-xxe-unsafe-xml-parser": _XXE_UNSAFE,
    "no-untrusted-component-sources": _UNTRUSTED_COMPONENTS,
    "no-insufficient-login-rate-limiting": _LOGIN_NO_LIMIT,
    "no-toctou-outside-lock": _TOCTOU,
    "no-missing-security-event-logging": _AUTH_HANDLER,
    "no-excessive-response-data": _EXCESSIVE_RESPONSE,
    "no-plaintext-sensitive-data-at-rest": _PLAINTEXT_SENSITIVE,
    "no-client-side-auth-trust": _CLIENT_AUTH_TRUST,
    "no-jwt-none-algorithm": _JWT_NONE,
}

CONTEXT_GATED_RULES = frozenset({"no-weak-crypto-algorithms"})


def patterns_for(rule_slug: str, language: Language) -> list[tuple[re.Pattern[str], str]]:
    """Return (regex, message) pairs applicable to the given language."""
    entries = CATALOG.get(rule_slug, [])
    out: list[tuple[re.Pattern[str], str]] = []
    for regex, message, langs in entries:
        if "all" in langs or language in langs:
            out.append((regex, message))
    return out


def context_gated_patterns(rule_slug: str, language: Language) -> list[tuple[re.Pattern[str], str]]:
    """Secondary patterns that require nearby security-context keywords."""
    if rule_slug != "no-weak-crypto-algorithms":
        return []
    out: list[tuple[re.Pattern[str], str]] = []
    for regex, message, langs in _WEAK_CRYPTO_CONTEXT:
        if "all" in langs or language in langs:
            out.append((regex, message))
    return out
