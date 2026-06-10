# Rule: Sources are verbatim excerpts with location

Every entry in `sources.md` must be a verbatim (or close-to-verbatim) excerpt from the code — the actual text the code contains — accompanied by the file path and line range. Inferences and pattern-name labels belong in the research path or deep-dive, not in source notes.

## DO

- Copy type definitions, function signatures, constant declarations, and comment text exactly as they appear in the source.
- Include a file path and line range on every excerpt.
- Add a brief factual observation line below an excerpt when a fact needs flagging (e.g. "P/Invoke at ViewModel level — no adapter").
- Keep observation lines short and factual; save interpretation and pattern naming for the deep-dive file.

## DO NOT

- Do not paraphrase code in plain English as a source note (e.g. writing "the method reads memory" instead of showing the actual signature).
- Do not omit the file path and line range from any excerpt.
- Do not include inferred pattern names or architectural judgments in the source note body — those belong in the deep-dive.

## Examples

**DO** — verbatim excerpt with location and brief factual observation:
```
### src/Crowds/CharacterExplorerViewModel.cs  lines 42–47
```csharp
[DllImport("kernel32.dll")]
static extern bool ReadProcessMemory(
    IntPtr hProcess, IntPtr lpBaseAddress,
    [Out] byte[] lpBuffer, int nSize, out int lpNumberOfBytesRead);
```
Observation: P/Invoke declaration at ViewModel level — no adapter layer.
```

**DO NOT** — paraphrase without code, no line range:
```
### CharacterExplorerViewModel
The class reads memory from the COH process using Windows kernel functions.
```
