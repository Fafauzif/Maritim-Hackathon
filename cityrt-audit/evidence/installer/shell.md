# Desktop shell forensics

## Verdict

`CityRT-Windows.exe` is an **installer**, not the game. Payload extraction was not possible
in this session (see limitation), but the shell identity is fully established from the PE
and the installer header.

| Fact | Value | Method |
|---|---|---|
| Format | PE32, i386, 5 sections, image base 0x400000 | header parse (`evidence/installer/recon/pe-dump.js`) |
| File size | 111,441,388 bytes | filesystem |
| SHA-256 | `d3975b27f5061b901abade2a03def8ee87ea9638e40e6b8631656e3b6dd996b6` | manifest |
| Import table | 7 DLLs, 165 imports, classic Win32 only (KERNEL32, USER32, GDI32, SHELL32, ADVAPI32, COMCTL32, ole32) | `inspect_pe_imports` |
| No graphics imports | no d3d/opengl/vulkan at load time | same |
| Overlay | 111,349,740 bytes starting at file offset 0x16600 | section table |
| Overlay signature | `0xDEADBEEF` + `NullsoftInst` → NSIS | hex dump |
| NSIS first-header size | 0x1DB52 (121,682 bytes) | header field |
| Installer build | Nullsoft Install System v3.04 (manifest string) | `.rsrc` |
| ProductName | `CityRT` | version resource |
| CompanyName | `CityRT.com` | version resource |
| FileDescription | "CityRT for Windows and macOS: a window onto cityrt.com, updates come from the site" | version resource |

## Interpretation

The description states the desktop build is a **window onto cityrt.com** with updates taken
from the site. Combined with the absence of any graphics-library import, the shell carries
no local renderer: it is a wrapper that loads the web client. This matches the site itself
serving an SSR marketing shell plus code-split chunks, with the game client behind login.

## Limitation (not a finding)

7-Zip could not be installed (`winget install 7zip.7zip` requires an interactive UAC
elevation, which this session cannot provide; winget reported installer exit code 1602,
"user cancelled"). Therefore the NSIS payload was **not** listed or extracted, and the
following remain unknown:

- whether the payload is Electron, NW.js, Tauri/WebView2, or a custom WebView shell;
- the bundled version string and auto-update feed;
- any preload/injected script or feature flags the shell adds.

None of these change the art-direction conclusion, which rests on the site's own renders.
The cheapest future probe is `7z l CityRT-Windows.exe` on a machine where 7-Zip is already
installed, or `7z x` into `evidence/installer/payload/`.
