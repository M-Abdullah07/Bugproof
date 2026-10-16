# Local tooling status

Verified October 16, 2026, Asia/Karachi.

- **Matt Pocock: installed.** 31 published skills in `.agents/skills`.
  All files match the official source snapshot after normalizing Windows
  line endings. See `mattpocock-install-verification.json`.
- **Gstack: instruction skills installed and registered.** Version
  1.91.101.0; 56 generated Codex skill entries. The local registry identifies
  the installation scope as `project`. Codex support is experimental upstream.
  Installed names use `gstack-` prefixes to avoid clashes with Matt's skills;
  the namespacing script reapplies this after setup.
- **Compiled gstack helpers: unavailable under current Windows policy.**
  Build artifacts were produced, but the `browse.exe --version` smoke check
  returned: “An Application Control policy has blocked this file.” Setup
  ultimately returned exit 126 after printing its installation summary.
  Full runtime readiness is therefore not confirmed. No OS policy was changed.
- **Gstack browser: deferred.** Chromium was deliberately not downloaded.
- **Gstack CSO native helper: unavailable.** Visual Studio C++ build tooling
  is absent. Do not treat an unassessed run as a security clearance.
- **Bun: verified.** Project-local executable reports 1.4.3.
- No skills were installed globally. No global Codex configuration was edited.
  Tool state, npm/Bun caches, and intended browser downloads are project-local.
- No MCP server or external account was installed/connected by this task.
  GitHub, Google Drive, and Trello are optional account-level suggestions.

Use the existing browser tools for QA in this environment. Installed planning,
specification, and review instructions can be read directly; skills needing
blocked native helpers must report that limitation instead of claiming success.

New skills should be available on the next turn. Reopen the project chat if
discovery has not refreshed.
