# UIA Tree Format (Windows Desktop)

**Full spec:** https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-uiautomationoverview  
**Control types reference:** https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-controltypesoverview

## What it is

UI Automation (UIA) is the Windows accessibility API. It exposes every control in a running Windows application as a tree of elements, each carrying:

- **Control type** — the Windows equivalent of an ARIA role (`Button`, `Edit`, `DataGrid`, `Window`, `Pane`)
- **Name** — the accessible label of the element
- **Properties** — value, enabled state, visibility, bounding rectangle

UIA works across Win32, WPF, WinForms, and UWP applications. It does not work for Electron apps with accessibility disabled or for purely canvas-rendered content.

## How it is captured

pywinauto wraps the UIA API. `window.print_control_identifiers()` dumps the full control tree for a window to a string. Save that string as `aria.yaml` under the matching page folder.

## Output format

`aria.yaml` for a Windows desktop surface is the raw pywinauto control identifier dump — an indented text tree, **not** WAI-ARIA YAML:

```
Dialog - 'Sign In'(L640, T360, R1280, B840)
   Pane - 'Content'(L640, T360, R1280, B840)
      Edit - 'Email address'(L700, T420, R1220, B450)
      Edit - 'Password'(L700, T470, R1220, B500)
      Button - 'Sign in'(L700, T520, R820, B550)
      Hyperlink - 'Forgot password?'(L840, T520, R980, B550)
```

Each line: `<ControlType> - '<Name>'(<BoundingRect>)`

This format is different from WAI-ARIA YAML. Downstream skills reading `aria.yaml` must check the `surface` field in `extraction-overview.md` to know which format to parse.

## What it does not capture

- Applications without UIA accessibility support (use pyautogui screenshot-only as fallback)
- Canvas-drawn content within a window
- Network payloads
