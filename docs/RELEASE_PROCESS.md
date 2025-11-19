# CloudSathi CLI - Release Process

This document describes how to create and publish releases of the CloudSathi CLI executable.

## Overview

The CloudSathi CLI uses GitHub Actions to automatically build executables for:
- **Linux** (amd64)
- **macOS** (amd64)
- **Windows** (amd64)

Executables are built using PyInstaller and published as GitHub Releases.

## Automated Release Process

### Creating a Release

1. **Update version** in `cli/__init__.py`:
   ```python
   __version__ = "1.1.0"
   ```

2. **Commit and push changes**:
   ```bash
   git add cli/__init__.py
   git commit -m "chore: bump version to 1.1.0"
   git push origin main
   ```

3. **Create and push a version tag**:
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

4. **GitHub Actions will automatically**:
   - Build executables for Linux, macOS, and Windows
   - Create a GitHub Release
   - Upload executables as release assets

### Workflow Details

The release workflow (`.github/workflows/release-cli.yml`) performs:

1. **Build Job** (runs on each platform):
   - Checks out code
   - Sets up Python 3.11
   - Installs dependencies
   - Builds executable with PyInstaller
   - Uploads artifact

2. **Release Job** (runs on Ubuntu):
   - Downloads all artifacts
   - Creates GitHub Release
   - Uploads executables as release assets

## Manual/Local Build

### Prerequisites

```bash
pip install pyinstaller
pip install -r backend/requirements.txt
```

### Build Executable

```bash
# Use the build script
./scripts/build-cli.sh

# Or manually with PyInstaller
pyinstaller cloudsathi.spec --clean
```

### Test Executable

```bash
# Linux/macOS
./dist/cloudsathi-* --version

# Windows
.\dist\cloudsathi-windows-*.exe --version
```

## PyInstaller Configuration

The `cloudsathi.spec` file configures:
- Entry point: `cli/main.py`
- Hidden imports for all CLI modules
- Single-file executable output
- Console application (not windowed)
- UPX compression enabled

## Release Checklist

Before creating a release:

- [ ] Update version in `cli/__init__.py`
- [ ] Update CHANGELOG.md (if exists)
- [ ] Test CLI locally
- [ ] Run all tests: `pytest tests/ -v`
- [ ] Commit version bump
- [ ] Create and push version tag
- [ ] Verify GitHub Actions workflow completes
- [ ] Test downloaded executables

## Troubleshooting

### Build Fails on GitHub Actions

**Check:**
1. Dependencies in `backend/requirements.txt` are correct
2. Hidden imports in `cloudsathi.spec` include all modules
3. GitHub Actions logs for specific errors

### Executable Doesn't Run

**Common issues:**
1. **Missing dependencies**: Add to `hiddenimports` in spec file
2. **File permissions** (Linux/macOS): Run `chmod +x cloudsathi-*`
3. **Antivirus blocking** (Windows): Add exception for executable

### Large Executable Size

**Solutions:**
1. Enable UPX compression (already enabled in spec)
2. Exclude unnecessary packages
3. Use `--exclude-module` for unused dependencies

## Distribution

### GitHub Releases

Users can download from: `https://github.com/saugat86/CloudSathi/releases`

### Installation Instructions

Include in release notes:

**Linux/macOS:**
```bash
# Download executable
wget https://github.com/saugat86/CloudSathi/releases/download/v1.0.0/cloudsathi-linux-amd64

# Make executable
chmod +x cloudsathi-linux-amd64

# Move to PATH
sudo mv cloudsathi-linux-amd64 /usr/local/bin/cloudsathi

# Verify
cloudsathi --version
```

**Windows:**
```powershell
# Download cloudsathi-windows-amd64.exe
# Rename to cloudsathi.exe
# Add directory to PATH or run from current directory

# Verify
.\cloudsathi.exe --version
```

## Version Numbering

Follow Semantic Versioning (SemVer):
- **Major** (1.0.0): Breaking changes
- **Minor** (1.1.0): New features, backwards compatible
- **Patch** (1.0.1): Bug fixes

## Future Enhancements

- [ ] Add ARM64 builds for Apple Silicon
- [ ] Add checksums (SHA256) for downloads
- [ ] Code signing for macOS and Windows
- [ ] Auto-update mechanism
- [ ] Homebrew formula for macOS
- [ ] Snap/AppImage for Linux
- [ ] Chocolatey package for Windows

---

For more information, see the [GitHub Actions documentation](https://docs.github.com/en/actions).
