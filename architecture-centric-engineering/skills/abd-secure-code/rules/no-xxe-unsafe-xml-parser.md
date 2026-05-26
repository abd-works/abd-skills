---
scanner: no_xxe_unsafe_xml_parser_scanner.py
category: df
---

# Rule: No XXE in unsafe XML parser configuration

XML parsers that resolve external entities or DTDs can leak files, perform SSRF, or cause denial of service. Disable DTDs and external entities on every parser that processes untrusted XML (CWE-611, OWASP A05).

## DO

- **DO** disable DTDs and external entity resolution on SAX/DOM/StAX parsers.

  **Example (pass):**

  ```java
  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
  factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
  factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
  ```

  **Example (pass):**

  ```python
  parser = defusedxml.ElementTree.parse(untrusted_stream)
  ```

- **DO** use defusedxml or equivalent hardening for Python; set `XMLConstants.FEATURE_SECURE_PROCESSING` where supported.

## DO NOT

- **DO NOT** parse untrusted XML with default parser settings.

  **Example (fail):**

  ```java
  Document doc = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(inputStream);
  ```

- **DO NOT** enable external DTD or XInclude on parsers handling request bodies.

  **Example (fail):**

  ```python
  etree.parse(untrusted_xml)  # lxml/xml.etree without defusedxml
  ```

**Source:** `context/green_belt_assessment/e0523/challenge-7.md`, `context/08_Software_or_Data_Integrity_Failures/exercises-challenges/Using-Components-From-Untrusted-Source.md`
