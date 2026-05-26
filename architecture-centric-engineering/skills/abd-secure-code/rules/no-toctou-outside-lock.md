---
scanner: no_toctou_outside_lock_scanner.py
category: ec
---

# Rule: No TOCTOU outside lock

When shared mutable state (balances, inventory, quotas) is read then written, the read and write must occur inside the same critical section. Checking a condition before acquiring a lock creates a time-of-check to time-of-use (TOCTOU) race (CWE-367).

## DO

- **DO** perform check and update inside the same lock, transaction, or atomic DB operation.

  **Example (pass):**

  ```java
  synchronized (sourceCard) {
      if (sourceCard.getBalance() < amount) throw new InsufficientFundsException();
      sourceCard.debit(amount);
      destCard.credit(amount);
  }
  ```

  **Example (pass):**

  ```sql
  UPDATE accounts SET balance = balance - :amt
  WHERE id = :id AND balance >= :amt;
  -- check rows affected == 1
  ```

## DO NOT

- **DO NOT** validate shared state outside a lock then modify inside it.

  **Example (fail):**

  ```java
  if (sourceCard.getBalance() < amount) return false;
  lock.lock();
  sourceCard.debit(amount);
  lock.unlock();
  ```

- **DO NOT** use read-modify-write on shared balances without transactions or row-level locking.

  **Example (fail):**

  ```python
  if account.balance < amount:
      return False
  with lock:
      account.balance -= amount
  ```

**Source:** `context/green_belt_assessment/e0523/challenge-10.md`, `context/10_Mishandling_of_Exceptional_Conditions/context/error-details.md` (concurrency section)
