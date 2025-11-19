# Changelog

All notable changes to CloudSathi will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Command-line interface (CLI) with Typer and Rich
- Standalone executables for Linux, macOS, and Windows
- Automated release pipeline with GitHub Actions
- Comprehensive testing guide and documentation
- CLI usage guide with examples

### Fixed
- Backend dependency issues (Pydantic v2, OpenSSL compatibility)
- Model path resolution in recommendation routes
- Azure routes indentation error
- Test variable naming mismatches
- GitHub Actions deprecated action warnings

### Changed
- Updated README with CLI-first approach
- Enhanced project structure documentation
- Improved error handling across all endpoints

### Documentation
- Added CLI Guide
- Added Testing Guide
- Added Release Process documentation
- Added CLI Walkthrough
- Added Test Report

---

## How to Update

This changelog is automatically generated from commit messages when creating releases.

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `perf`: Performance improvements
- `test`: Test additions or changes
- `refactor`: Code refactoring

**Examples:**
```
feat(cli): add AWS costs command
fix(api): resolve date validation error
docs: update README with CLI information
ci: add changelog generation workflow
```

---

*This changelog is automatically generated. Do not edit manually.*
