# Draw.io Diagram Embedding in Markdown

## Rule

Whenever you link a `.drawio` file from a Markdown document, you must also:

1. **Export a PNG** from the same `.drawio` file — same name, same folder, `.png` extension.
2. **Embed the PNG** as an inline image immediately below the drawio source link.

## Format

```markdown
> Source: [`{name}.drawio`](./{name}.drawio).

![{Diagram title}](./{name}.png)
```

## Example

```markdown
> Source: [`architecture-flow.drawio`](./architecture-flow.drawio).

![Architecture Flow](./architecture-flow.png)
```

## How to export the PNG

From Draw.io Desktop:
- **File → Export As → PNG…** — check "Fit page", uncheck "Shadow", click Export.
- Save to the same folder as the `.drawio` file with the same base name.

Or from the command line (requires `drawio` npm package):

```powershell
drawio --export --format png --output {same-folder}/{name}.png {same-folder}/{name}.drawio
```

## Exporting the PNG — agent responsibility

When you create or edit a `.drawio` file, you must also export the PNG yourself. Do not wait for the user to do it. Use the `drawio` CLI:

```powershell
drawio --export --format png --output {same-folder}/{name}.png {same-folder}/{name}.drawio
```

If `drawio` is not on PATH, find the executable:

```powershell
# Common Windows locations
& "C:\Program Files\draw.io\draw.io.exe" --export --format png --output {out}.png {in}.drawio
& "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" --export --format png --output {out}.png {in}.drawio
```

The PNG must exist on disk before the Markdown file is committed. Do not leave a broken image reference.

## Why

Standard VS Code preview and GitHub do not render `.drawio` files inline. A co-located PNG ensures the diagram is visible in any Markdown viewer without extensions.
