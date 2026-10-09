"""Exercise real ZIP and Debian builds without installing into the running session."""

import hashlib
import importlib.util
import io
import json
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_release", ROOT / "scripts/package-release.py")
PACKAGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGER)


class ReleasePackageTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.build = self.root / "build"
        self.output = self.root / "dist"
        self.build.mkdir()
        self.metadata = json.loads((ROOT / "extension/metadata.json").read_text())
        (self.build / "metadata.json").write_text(json.dumps(self.metadata))
        for name in ("extension.js", "prefs.js", "LICENSE", "schemas/gschemas.compiled", "locale/nl/LC_MESSAGES/brightness-restore.mo"):
            path = self.build / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"fixture\n")
            path.chmod(0o600)

    def test_installable_payload_and_checksums(self):
        PACKAGER.package(self.build, self.output, "4.0.0")
        deb = self.output / "gnome-shell-extension-brightness-restore-tiagosantosvdl_4.0.0_all.deb"
        fields = subprocess.check_output(["dpkg-deb", "--field", str(deb)], text=True)
        self.assertIn("Architecture: all\n", fields)
        self.assertIn("gnome-shell (>= 45~), gnome-shell (<< 51~)", fields)
        self.assertIn("Version: 4.0.0\n", fields)
        unpacked = self.root / "unpacked"
        subprocess.run(["dpkg-deb", "--extract", str(deb), str(unpacked)], check=True)
        installed = unpacked / "usr/share/gnome-shell/extensions" / self.metadata["uuid"]
        with ZipFile(next(self.output.glob("*.zip"))) as archive:
            self.assertIn("extension.js", archive.namelist())
            self.assertIn("schemas/gschemas.compiled", archive.namelist())
            metadata = json.loads(archive.read("metadata.json"))
            self.assertEqual(metadata["uuid"], "brightness-restore@tiagosantosvdl.github.com")
            self.assertEqual(metadata["version-name"], "4.0.0")
            self.assertEqual(metadata["version"], self.metadata["version"])
            for name in archive.namelist():
                self.assertEqual(archive.read(name), (installed / name).read_bytes())
        payload = subprocess.check_output(["dpkg-deb", "--fsys-tarfile", str(deb)])
        with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
            for member in archive:
                self.assertEqual((member.uid, member.gid), (0, 0))
                self.assertEqual(member.mode, 0o755 if member.isdir() else 0o644)
        for line in (self.output / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ")
            self.assertEqual(digest, hashlib.sha256((self.output / name).read_bytes()).hexdigest())
        self.assertEqual(json.loads((self.build / "metadata.json").read_text()), self.metadata)

    def test_prerelease_sorts_before_stable(self):
        PACKAGER.package(self.build, self.output, "4.0.0-rc.1")
        deb = self.output / "gnome-shell-extension-brightness-restore-tiagosantosvdl_4.0.0~rc.1_all.deb"
        self.assertTrue(deb.is_file())
        subprocess.run(["dpkg", "--compare-versions", "4.0.0~rc.1", "lt", "4.0.0"], check=True)

    def test_invalid_version_does_not_create_artifacts(self):
        for version in ("../escape", "v4.0.0", "4", "4.00", "4.0.0+build", "4.0.0-verylongprerelease"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                PACKAGER.package(self.build, self.output, version)
        self.assertFalse(self.output.exists())

    def test_missing_compiled_schema_fails(self):
        (self.build / "schemas/gschemas.compiled").unlink()
        with self.assertRaisesRegex(ValueError, "Missing schemas/gschemas.compiled"):
            PACKAGER.package(self.build, self.output, "4.0.0")

    def test_patch_version_supported(self):
        PACKAGER.package(self.build, self.output, "4.0.1")
        self.assertTrue((self.output / "gnome-shell-extension-brightness-restore-tiagosantosvdl_4.0.1_all.deb").is_file())

    def test_invalid_integer_version_fails(self):
        for version in ("4", 4.1, True, 0):
            with self.subTest(version=version):
                metadata = {**self.metadata, "version": version}
                (self.build / "metadata.json").write_text(json.dumps(metadata))
                with self.assertRaisesRegex(ValueError, "positive integer"):
                    PACKAGER.package(self.build, self.output, "4.0.0")
        self.assertFalse(self.output.exists())

    def test_noncontiguous_shell_versions_fail(self):
        for shells in ([], ["46", "48"]):
            with self.subTest(shells=shells):
                metadata = {**self.metadata, "shell-version": shells}
                (self.build / "metadata.json").write_text(json.dumps(metadata))
                with self.assertRaisesRegex(ValueError, "contiguous"):
                    PACKAGER.package(self.build, self.output, "4.0.0")
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
