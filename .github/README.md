# Brightness Restore

This is [@tiagosantosvdl's fork](https://github.com/tiagosantosvdl/brightness-restore) of [Brightness Restore by @DarkPhilosophy](https://github.com/DarkPhilosophy/brightness-restore), a GNOME Shell extension that saves brightness adjustments and restores them on login. This fork is maintained with OpenAI Codex and provides its own extension packages.

[![Extension CI](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/ci.yml/badge.svg)](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/ci.yml)
[![Release packages](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/release.yml/badge.svg)](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/release.yml)
<!-- GNOME-SHELL-VERSIONS-START --> [![GNOME 45-50](https://img.shields.io/badge/GNOME-45--50-blue.svg)](https://www.gnome.org/) <!-- GNOME-SHELL-VERSIONS-END --> [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](../LICENSE)

## Project status

The fork hides its indicator and brightness slider when brightness control is unavailable. Invalid readings do not replace saved brightness or trigger brightness writes. Version **4.0.1** standardizes the release package filenames.

- Extension UUID: `brightness-restore@tiagosantosvdl.github.com`.
- Supported GNOME Shell versions: **45–50**, as declared in [metadata.json](../extension/metadata.json).
- Settings schema: `org.gnome.shell.extensions.brightness-restore`, preserving existing preferences.

Declared compatibility is not a completed test matrix for every GNOME version or monitor. Automated packaging tests, source syntax checks, and schema validation are available; full desktop compatibility remains unverified. Repository changes take effect only after rebuilding, installing, and loading the new code in GNOME Shell.

The [GNOME Extensions listing](https://extensions.gnome.org/extension/9214/brightness-restore/) belongs to upstream. Install this fork from this repository's releases or source.

## Features

- Save brightness adjustments and optionally restore the saved value on login.
- Use GNOME Shell's brightness manager when available, with a SettingsDaemon D-Bus fallback.
- Show brightness in the panel's Quick Settings area or in a standalone menu with a slider.
- Hide the indicator and standalone slider when brightness is unavailable, including negative or missing readings. Zero brightness remains valid.
- Configure the indicator's position.
- Blank the screen after an optional idle timeout, using a black overlay or Mutter's display power control, and restore it on activity.
- Provide debug logging and manual screen-off controls in preferences.

Brightness adjustment depends on the backend exposed by GNOME; installing the extension does not add brightness support to an unsupported display.

## Installation

Download packages from this repository's [GitHub Releases](https://github.com/tiagosantosvdl/brightness-restore/releases). Each release includes an extension ZIP, a Debian package, and `SHA256SUMS`.

Disable the upstream extension before enabling this fork. Choose one installation method: a per-user copy takes precedence over a system-wide copy with the same UUID. Remove an existing per-user copy of the fork when switching to the Debian package so it does not shadow the installed update.

### Debian / Ubuntu package

For release `4.0.1`, install the downloaded package:

```sh
sudo apt install ./gnome-shell-extension-brightness-restore-tiagosantosvdl_4.0.1_all.deb
```

The package is architecture-independent and declares dependencies on GNOME Shell 45–50 and `gir1.2-adw-1`. It installs under `/usr/share/gnome-shell/extensions/brightness-restore@tiagosantosvdl.github.com/`.

Log out and back in after installation or an upgrade so GNOME discovers the extension and loads the installed code. Enable it with:

```sh
gnome-extensions enable brightness-restore@tiagosantosvdl.github.com
```

### Per-user ZIP

Install the downloaded ZIP:

```sh
gnome-extensions install --force ./brightness-restore@tiagosantosvdl.github.com-4.0.1.zip
```

Install libadwaita's introspection bindings (`gir1.2-adw-1` on Debian / Ubuntu) for preferences. Log out and back in, then enable the extension using the same command as for the Debian package.

The fork's UUID differs from upstream's `brightness-restore@DarkPhilosophy`; installation does not replace upstream automatically. Both use the same settings schema, so saved preferences are retained.

### Verify downloads

Place `SHA256SUMS` and both release packages in the same directory, then run:

```sh
sha256sum -c SHA256SUMS
```

### Open preferences

```sh
gnome-extensions prefs brightness-restore@tiagosantosvdl.github.com
```

If GNOME reports that the extension does not exist immediately after installing the Debian package, check the installed package with `dpkg-query -W gnome-shell-extension-brightness-restore-tiagosantosvdl`, then log out and back in. Package installation and discovery by the running Shell are separate steps.

## Build from source

Install Git, Node.js, Python 3, Make, `glib-compile-schemas` (`libglib2.0-bin` on Debian / Ubuntu), and `dpkg-deb` (`dpkg`). Clone this repository and build:

```sh
git clone https://github.com/tiagosantosvdl/brightness-restore.git
cd brightness-restore
make release
```

Building packages stages the extension under `_build/` without installing or activating it. For version `4.0.1`, the output is:

- `dist/brightness-restore@tiagosantosvdl.github.com-4.0.1.zip`
- `dist/gnome-shell-extension-brightness-restore-tiagosantosvdl_4.0.1_all.deb`
- `dist/SHA256SUMS`

Verify and install the local Debian build:

```sh
(cd dist && sha256sum -c SHA256SUMS)
sudo apt install ./dist/gnome-shell-extension-brightness-restore-tiagosantosvdl_4.0.1_all.deb
```

Then log out and back in and enable the extension as described above.

The legacy `./build.sh` command builds and installs a per-user copy and changes extension/schema state. It requires npm development dependencies. `./package.sh` produces an unversioned extension ZIP and also applies lint fixes, formatting, and version/documentation updates. Use `make release` to build release packages without those side effects.

## Configuration and logs

Open preferences to change behavior, appearance, brightness, idle timeout, and debug options. Existing saved settings take precedence over these repository defaults.

| Setting | Default | Behavior |
| --- | --- | --- |
| Restore on Startup | `true` | Restore the last valid saved brightness on login. |
| Indicator Style | `quick-settings` | Show a panel percentage in Quick Settings, or choose `standalone` for a menu with a slider. |
| Indicator Position | `right` | Choose `left`, `right`, or `default`. |
| Last Brightness | `-1.0` | Normalized saved value from 0 to 1; `-1.0` means unset. |
| Update Interval | `2` seconds | Exposed in preferences; the runtime currently uses a fixed one-second save debounce. |
| Enable Idle Timeout | `false` | Blank the screen after the configured idle duration. |
| Idle Duration | `300` seconds | Five minutes by default. |
| Timeout Action | `overlay` | Black overlay, or `dbus` for display power control. |
| Enable Debug | `false` | Enable extra logging and manual screen controls. |
| Log Level | `1` | 0=Verbose, 1=Debug, 2=Info, 3=Warn, 4=Error. |
| Save Logs to File | `true` | File logging preference; log output also depends on debug mode. |
| Log File Path | Empty | Use the cache directory unless a custom path is provided. |

The default log file is `$XDG_CACHE_HOME/brightness_restore.log`, normally `~/.cache/brightness_restore.log`. Debug preferences include manual screen-off testing with overlay or D-Bus mode; user activity restores the screen.

Follow extension messages with:

```sh
journalctl --user --follow --output=short-iso --grep 'Brightness Restore'
```

Review logs before sharing them, and include only messages relevant to the reported problem.

## Development and verification

Runtime source lives in `extension/`, support code in `extension/library/`, indicator actors in `extension/library/indicators/`, and schemas in `extension/schemas/`. Packaging uses the [Makefile](../Makefile) and [scripts/package-release.py](../scripts/package-release.py). Agent guidance is in [AGENTS.md](../AGENTS.md).

Run checks relevant to your change:

```sh
node --input-type=module --check < extension/extension.js
node .scripts/validate-build.js
node .scripts/scan-leaks.js
glib-compile-schemas --strict --dry-run extension/schemas
python3 -m unittest discover -s tests -p '*test.py'
git diff --check
```

Syntax-check every changed JavaScript file using ES module parsing. Packaging tests build real ZIP and Debian packages without installing them, check payloads and checksums, and verify permissions, version validation, and prerelease ordering.

For ESLint, install development dependencies and invoke it directly:

```sh
npm ci
npx eslint extension .scripts --format stylish
```

The current `npm run lint` and `npm run lint:fix` scripts suppress ESLint failures, so their successful exit status is not proof that lint passed. The latter also rewrites files.

Validate desktop behavior separately: supported and unsupported brightness backends, zero brightness, login restoration, both indicator styles, changing settings, and idle blanking/wake behavior. Automated checks do not prove live GNOME behavior.

## Releases

Update `package.json`, run `node .scripts/sync-version.js`, and inspect the resulting changes to `package-lock.json`, `extension/metadata.json`, `VERSION`, preferences, and documentation. Update installation examples in this README and relevant [changelog entries](CHANGELOG.md).

Release tags must match the package version, such as `v4.0.1`. Metadata's `version-name` contains the full release version; its integer `version` and the `VERSION` file currently derive from the package's major version.

The [release workflow](workflows/release.yml) checks source syntax, schemas, packaging, version consistency, and checksums. It publishes packages when a matching version tag is pushed or a GitHub Release is published. The manual **Run workflow** option builds downloadable artifacts without publishing a release.

After checking, building, and committing the release changes, create an annotated tag and push it with the branch:

```sh
git tag -a v4.0.1 -m "Brightness Restore 4.0.1"
git push --atomic origin main v4.0.1
```

Use a new version for each release; do not replace an existing published tag. Confirm the workflow succeeded and the release assets are available before announcing publication.

Release filenames follow the same convention as the neighboring extension forks: `<uuid>-<version>.zip`, `gnome-shell-extension-<name>-tiagosantosvdl_<debian-version>_all.deb`, and `SHA256SUMS`. Prerelease tags such as `v4.0.1-rc.1` use `version-name` `4.0.1 rc.1`, ZIP version `4.0.1-rc.1`, and Debian version `4.0.1~rc.1`.

## Issues and contributions

Report bugs and request features in [this repository's issue tracker](https://github.com/tiagosantosvdl/brightness-restore/issues). Include your distribution, GNOME Shell and extension versions, session type, monitor arrangement, whether GNOME exposes brightness control, reproduction steps, and relevant Shell logs.

Submit changes through [pull requests](https://github.com/tiagosantosvdl/brightness-restore/pulls), with a description of the behavior changed and verification performed. See the [contributing guide](CONTRIBUTING.md) and [changelog](CHANGELOG.md).

## Credits and licensing

This fork builds on Brightness Restore by [@DarkPhilosophy](https://github.com/DarkPhilosophy) and its contributors. Upstream project and donation links remain available through [the original repository](https://github.com/DarkPhilosophy/brightness-restore).

Licensed under GPL-3.0-or-later; see [LICENSE](../LICENSE).
