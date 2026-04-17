# Vendored wheels (offline installs)

This folder holds **Python wheels** (and occasional source tarballs) so a machine **without PyPI access** can still install everything in `../requirements-all.txt`.

## Populate wheels (on a machine with internet)

From **repository root** or from this agent folder:

```powershell
cd agents/abd-context-engine
python -m pip download -r requirements-all.txt -d vendor/wheels
```

To refresh after editing `requirements-all.txt`, delete old wheels or use a clean `vendor/wheels` folder.

## Install on an offline machine

Copy the whole `agents/abd-context-engine` tree (including `vendor/wheels`). Then:

```powershell
cd agents/abd-context-engine
python -m pip install --no-index --find-links vendor/wheels -r requirements-all.txt
```

Use the **same Python version** (e.g. 3.10+) and **platform** (Windows/macOS/Linux) as the machine that ran `pip download`, or download wheels per target with `pip download`’s `--platform` / `--python-version` flags.

## Size

`markitdown[all]` pulls many transitive packages; `vendor/wheels` may be **hundreds of MB**. If you prefer not to commit binaries, keep wheels on an internal artifact share and copy them next to this folder before offline install.
