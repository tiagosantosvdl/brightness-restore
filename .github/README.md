# Brightness Restore for GNOME Shell

[![Extension CI](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/ci.yml/badge.svg)](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/ci.yml)
[![Release packages](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/release.yml/badge.svg)](https://github.com/tiagosantosvdl/brightness-restore/actions/workflows/release.yml)
<!-- GNOME-SHELL-VERSIONS-START --> [![GNOME 45-50](https://img.shields.io/badge/GNOME-45--50-blue.svg)](https://www.gnome.org/) <!-- GNOME-SHELL-VERSIONS-END --> [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## About this fork

This is [@tiagosantosvdl's fork](https://github.com/tiagosantosvdl/brightness-restore) of [Brightness Restore by @DarkPhilosophy](https://github.com/DarkPhilosophy/brightness-restore), maintained with Codex. Report issues with this fork in [this repository's issue tracker](https://github.com/tiagosantosvdl/brightness-restore/issues).

The fork uses the extension UUID `brightness-restore@tiagosantosvdl.github.com` and shares the original settings schema and saved preferences. The [GNOME Extensions listing](https://extensions.gnome.org/extension/9214/brightness-restore/) belongs to the upstream project; install this fork from its GitHub releases or source.

**Brightness Restore** - A GNOME Shell extension that solves the "missing persistence" issue for software brightness controls (especially on external monitors combined with OLED/Wayland setups).

It automatically saves your local brightness adjustments and restores them upon login, ensuring your preferred brightness level is always maintained.

## Features

-   **Persistence**: Automatically saves the last known brightness level to disk.
-   **Auto-Restore**: Applies the saved brightness level immediately upon session startup.
-   **Integration**: Connects directly to Gnome Shell's internal `brightnessManager`.
-   **Indicator**: Shows a simple percentage indicator in the panel (configurable).
-   **Unavailable Brightness**: Hides the indicator and brightness slider when brightness control is unavailable.
-   **Positioning**: Choose to place the indicator on the Left or Right of the QuickSettings area.

## Validation Status

<!-- LINT-RESULT-START -->
### Linting Status
> **Status**: ✅ **Passing**  
> **Last Updated**: 2026-10-09 14:00:44 UTC  
> **Summary**: 0 errors, 0 warnings

<details>
<summary>Click to view full lint output</summary>

```text
> brightness-restore@4.0.1 lint:fix
> eslint --fix extension .scripts --format stylish || true; echo LINT_DONE

LINT_DONE
```

</details>
<!-- LINT-RESULT-END -->

<!-- LATEST-VERSION-START -->
<details open>
<summary><strong>Latest Update (v4)</strong></summary>

- Add the new extension icon asset for the next release cycle.
- Add Idle Screen Timeout settings and runtime screen-off actions.
- Add 10-second timeout option for fast testing from preferences.
- Add manual Screen Control test path handled by the shell process.
- Fix overlay and D-Bus wake/sleep behavior to avoid freezes and delayed triggers.

</details>
<!-- LATEST-VERSION-END -->

## Configuration

You can configure the extension using standard Gnome Extensions settings (or `dconf`).

### General

| Setting | Default | Description |
| :--- | :--- | :--- |
| **Restore on Startup** | `true` | Whether to restore the saved value on login. |
| **Indicator Style** | `quick-settings` | `standalone` (Panel Button) or `quick-settings` (Pill). |
| **Indicator Position** | `right` | `left`, `right`, or `default` (Only for Quick Settings). |
| **Interval** | `2` | Internal update interval (debounced save). |
| **Last Brightness** | `-1.0` | Last saved brightness value. `-1.0` means unset. |

### Idle Screen Timeout

| Setting | Default | Description |
| :--- | :--- | :--- |
| **Enable Idle Timeout** | `false` | Automatically blank the screen after the configured idle period. |
| **Idle Duration** | `300` (`5 minutes`) | Time in seconds before the idle timeout triggers. |
| **Timeout Action** | `overlay` | Screen blank method: `overlay` or `dbus`. |

### Debug

| Setting | Default | Description |
| :--- | :--- | :--- |
| **Enable Debug** | `false` | Enable debug-only controls and extra logging. |
| **Log Level** | `1` | 0=Verbose, 1=Debug, 2=Info, 3=Warn, 4=Error. |
| **Log to File** | `true` | Write debug logs to file. |
| **Log File Path** | `''` | Custom path for the log file. Empty uses the default cache path. |
| **Screen Test Action** | `overlay` | Manual screen blank test mode used by the debug Screen Control action. |
| **Screen Test Sequence** | `0` | Internal counter incremented to request a new manual screen test. |

## Install

### GitHub Releases

Download the ZIP or Debian package from [Releases](https://github.com/tiagosantosvdl/brightness-restore/releases). Each release includes `SHA256SUMS`; verify downloads with `sha256sum -c SHA256SUMS` after downloading both packages and the checksum file into the same directory.

Install the ZIP with GNOME's extension tool (replace the version as needed):

```bash
gnome-extensions install --force brightness-restore@tiagosantosvdl.github.com-4.0.1.zip
```

On Debian or Ubuntu with GNOME Shell 45–50, install the Debian package:

```bash
sudo apt install ./gnome-shell-extension-brightness-restore-tiagosantosvdl_4.0.1_all.deb
```

Log out and back in after installation. Disable the upstream Brightness Restore extension if installed, then enable the fork:

```bash
gnome-extensions enable brightness-restore@tiagosantosvdl.github.com
```

### Local Build

```bash
./build.sh
```

### Manual

Copy the contents of `extension/` to `~/.local/share/gnome-shell/extensions/brightness-restore@tiagosantosvdl.github.com`, then compile the schemas in that directory with `glib-compile-schemas`.

## Building releases

Install Python 3, Node.js, Make, `glib-compile-schemas` (Debian package `libglib2.0-bin`), and `dpkg-deb` (`dpkg-dev`), then run:

```bash
make release
```

This stages the extension without installing it and writes a versioned ZIP, an architecture-independent Debian package, and `SHA256SUMS` to `dist/`. The packages include compiled schemas and the license.

Release filenames follow the same convention across these extensions: `<uuid>-<version>.zip`, `gnome-shell-extension-<name>-tiagosantosvdl_<debian-version>_all.deb`, and `SHA256SUMS`. Debian prerelease versions use `~rc.1` where ZIP versions use `-rc.1`.

The [release workflow](workflows/release.yml) follows the same pattern as the ArcMenu, Forge, and Dash to Panel forks:

- Pushing a `v*` tag builds the packages and creates a GitHub release, or updates its assets if the release already exists.
- Publishing a GitHub release builds packages from its tag and attaches them to that release.
- Running the workflow manually builds the selected ref and uploads downloadable artifacts without publishing a release.

Before tagging a release, update `package.json` and run `node .scripts/sync-version.js` to synchronize `package-lock.json`, `extension/metadata.json`, and `VERSION`. The tag must match the package version, such as `v4.0.1`. Tags containing a prerelease suffix, such as `v4.0.1-rc.1`, create prereleases. The numeric GNOME extension version remains separate from the full release version in `version-name`.

Validate packaging locally with:

```bash
python3 -m unittest discover -s tests -p '*test.py'
```

## Contributing

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](../LICENSE)
