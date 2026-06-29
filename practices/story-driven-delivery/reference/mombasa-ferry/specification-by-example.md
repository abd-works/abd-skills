# Mombasa Ferry Service — Specification by Example

Reference specification for the `abd-story-specification` skill. Covers two stories from Increment 1 and Increment 3. Used as a quality bar and grill-me scenario. See [`README.md`](./README.md) for domain context and [`acceptance-criteria.md`](./acceptance-criteria.md) for the AC source.

---

## Story: Present Journey Card

**Feature:** Manage Passenger Crossing / Pay Fare

### Background

    Given a **Vessel** *MV Likoni* is open for boarding  
    And the current **Fare** is *KES 50*

---

### Scenario Outline: Passenger boards on valid Journey Card

    When a **Passenger** *{passenger_name}* presents **Journey Card** *{card_id}* with **Balance** *{starting_balance}*  
    Then the system deducts **Fare** *KES 50* from the card  
    And the **Balance** on *{card_id}* is *{remaining_balance}*  
    And *{passenger_name}* is admitted to the **Boarding Queue**  
    And the **Payment Terminal** displays **Balance** *{remaining_balance}*  

    Examples: Journey Card — balances
    | passenger_name | card_id    | starting_balance | remaining_balance |
    |----------------|------------|-----------------|-------------------|
    | Amina Oduya    | KFS-0042   | KES 200          | KES 150           |
    | Baraka Mwangi  | KFS-1187   | KES 50           | KES 0             |
    | Chebet Kiprotich | KFS-0883 | KES 500          | KES 450           |

---

### Scenario Outline: Passenger rejected for insufficient balance

    When a **Passenger** *{passenger_name}* presents **Journey Card** *{card_id}* with **Balance** *{starting_balance}*  
    Then the system rejects the **Fare** deduction  
    And the **Payment Terminal** displays **Balance** *{starting_balance}* and shortfall *{shortfall}*  
    And *{passenger_name}* is not admitted to the **Boarding Queue**  
    And the **Balance** on *{card_id}* remains *{starting_balance}*  

    Examples: Journey Card — insufficient balance
    | passenger_name | card_id   | starting_balance | shortfall |
    |----------------|-----------|-----------------|-----------|
    | David Otieno   | KFS-2210  | KES 30           | KES 20    |
    | Esther Kamau   | KFS-0055  | KES 0            | KES 50    |

---

### Scenario Outline: Passenger rejected for blocked or expired card

    When a **Passenger** *{passenger_name}* presents **Journey Card** *{card_id}* with status *{card_status}*  
    Then the system rejects the card  
    And the **Payment Terminal** displays reason *{rejection_reason}*  
    And the **Balance** on *{card_id}* is unchanged  
    And *{passenger_name}* is not admitted to the **Boarding Queue**  

    Examples: Journey Card — invalid card states
    | passenger_name | card_id   | card_status | rejection_reason |
    |----------------|-----------|-------------|-----------------|
    | Francis Njoroge | KFS-7701 | blocked     | Card blocked — contact KFS |
    | Grace Wanjiku  | KFS-0012  | expired     | Card expired — reissue required |

---

## Story: Close Boarding At Capacity

**Feature:** Manage Passenger Crossing / Board Vessel

### Background

    Given a **Vessel** *MV Pwani* is open for boarding  
    And **Capacity** is *120 passengers*  

---

### Scenario: Boarding closes automatically at capacity

    When the **Boarding Count** reaches *120*  
    Then the system marks **Vessel** *MV Pwani* as *Full*  
    And boarding is closed automatically  
    And passengers remaining in the **Boarding Queue** are held for the next **Crossing**  

---

### Scenario Outline: Operator manually closes boarding before capacity

    Given **Boarding Count** is *{current_count}* of *120*  
    When the **Ferry Operator** *{operator_name}* manually closes boarding  
    Then the system records **Boarding Count** as *{current_count}*  
    And the **Vessel** is not marked as *Full*  
    And no further passengers may board this **Crossing**  
    And the **Boarding Queue** for the next **Crossing** remains open  

    Examples: Manual close
    | operator_name    | current_count |
    |-----------------|---------------|
    | Operator Hassan  | 98            |
    | Operator Nafula  | 115           |

---

## What to notice

- **Scenario Outline** is the default for every story with data variation — not plain Scenario
- **Background** holds state shared by three or more scenarios (`Given` only — no `When` or `Then`)
- Table columns express **domain relationships** — `passenger_name` and `card_id` appear together because they belong to the same **Journey Card** concept
- Example values are **realistic domain data**: Kenyan names, KFS card IDs, KES currency, real capacity numbers
- The auto-close scenario is a **plain Scenario** (one structural path, no data variation worth parameterising)
- **Bold** on domain concepts; *italics* on their values — applied consistently throughout
- Trailing two spaces on every step line render each step on its own line in Markdown preview
