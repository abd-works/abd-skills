# Rule: Generated code matches spec file layout

Every generated file must land in the folder, use the naming pattern, and respect the layer placement defined in **`<spec-root>`** (`architecture-specification.md` and `template/`) — where **`<spec-root>`** is the architecture spec path resolved in step 0, not a fixed path in this skill.

## DO

- Place each file in the directory the spec prescribes for its layer.

  **Example (pass):** For `specs/hero-vtt` — `CharacterViewModel.cs` in `Module.HeroVirtualTabletop/Characters/`; test in `Module.UnitTest/Presentation/`; never swapped.

- Name files by substituting the story's domain terms into the spec template filenames (`specs/<arch>/templates/{DomainName}.cs` → `Character.cs`).

  **Example (pass):** Template `{domainName}.routes.ts` with domain `recipient` → `recipient.routes.ts` in the server package.

- Match the spec example's folder hierarchy exactly — do not flatten or invent sub-folders.

  **Example (pass):** `specs/mern` example has `packages/{domainName}/shared/`, `server/`, `client/` — generated module uses the same three sub-folders with the same file split.

## DO NOT

- Put domain or seam files in a layer the spec does not assign them to.

  **Example (fail):** `IGameCommandExecutor.cs` placed inside `Module.HeroVirtualTabletop/Characters/` — spec places all seam interfaces in `Library/GameCommunicator/`.

- Invent file or folder names not derivable from the spec templates and domain terms.

  **Example (fail):** `CharacterService.cs` created alongside `Character.cs` when no `{Domain}Service.cs` template exists in `specs/hero-vtt/templates/`.
