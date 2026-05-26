---
scanner: no_sql_string_concatenation_scanner.py
category: if
---

# Rule: No SQL string concatenation

Production database access must separate SQL structure from user-supplied data. Passing through bound parameters or an ORM's safe API passes; building SQL with string concatenation, f-strings, or `.format()` with untrusted values fails because the database cannot distinguish code from data.

## DO

- **DO** use parameterized queries / prepared statements for every dynamic value in SQL.

  **Example (pass):**

  ```python
  cur.execute("SELECT balance FROM accounts WHERE user_name = %s", (customer_name,))
  ```

  **Example (pass):**

  ```javascript
  await pool.query('SELECT balance FROM accounts WHERE user_name = $1', [customerName]);
  ```

  **Example (pass):**

  ```java
  PreparedStatement ps = conn.prepareStatement(
      "SELECT balance FROM accounts WHERE user_name = ?");
  ps.setString(1, customerName);
  ```

- **DO** allow-list dynamic identifiers (table, column, sort direction) when they cannot be bound.

  **Example (pass):** Map `sort=price` to a fixed enum `ORDER BY price ASC` — never interpolate raw user strings into identifier positions.

## DO NOT

- **DO NOT** concatenate or interpolate user input into SQL text.

  **Example (fail):**

  ```python
  query = f"SELECT * FROM users WHERE name = '{username}'"
  cur.execute(query)
  ```

- **DO NOT** use ORM `raw()` / string SQL with embedded variables.

  **Example (fail):**

  ```javascript
  db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
  ```

- **DO NOT** build JDBC SQL with string concatenation or `String.format`.

  **Example (fail):**

  ```java
  stmt.executeQuery("SELECT * FROM users WHERE name = '" + username + "'");
  ```

**Source:** `context/05-injection-flaws/context/sql-injection-prevention-cheat-sheet.md`, `context/05-injection-flaws/exercises-challenges/sql-injection.md`
