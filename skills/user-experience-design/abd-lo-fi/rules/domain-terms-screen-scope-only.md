# Rule: Only domain terms whose stories appear on this screen may be on the canvas

**Scanner:** AI review

The wireframe is for **one** screen. Only the domain terms whose stories are attached to that screen (user-visible stories plus its grouped system stories) may appear on the canvas. Terms that belong to other screens, however interesting, are out of scope.

## DO

- Build the canvas's term set from the in-scope story list, intersected with the UL file. Anything outside that intersection stays off the canvas.

  **Example (pass):** The `game directory prompt` screen has stories *Validate City of Heroes Game Directory* and *Prompt for Game Directory if Invalid*. These stories reference `COH game directory`, `crowd repository`, `crowd manager` (as the target of a redirect). Only those terms appear on the canvas.

- When in doubt, search the in-scope story text for the term. If no in-scope story references it, leave it off.

## DO NOT

- Pull in a term because it is "central" to the domain.

  **Example (fail):** Adding `clipboard`, `flatten-copy`, or `gang mode` to the `game directory prompt` wireframe because they are in the UL. None of its stories use them.

- Pull in a term to "give the wireframe more context".

  **Example (fail):** Showing every UL term as a legend on the side of the canvas. The wireframe should read like the screen, not like the UL file.

- Include a term that appears only in another screen's stories.

  **Example (fail):** Putting `character detail panel` on the `game directory prompt` wireframe because that term shows up on the `crowd manager` screen.
