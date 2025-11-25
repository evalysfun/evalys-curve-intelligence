# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation (curve-spec.md, detection.md, risk-model.md, evaluation.md)
- Runnable demo script (examples/demo.py)
- CHANGELOG.md and ROADMAP.md

### Changed
- Updated README with honest staging (Implemented vs Planned)
- Fixed Windows path formatting in README

## [0.1.0] - 2024-01-XX

### Added
- Initial release of Curve Intelligence Layer
- Curve analysis with slope, liquidity depth, trade velocity, volatility metrics
- Sniper detection algorithm (v0.1)
- Buy cluster detection algorithm (v0.1)
- Risk assessment with weighted formula
- Pattern recognition (whales, bots, pump/dump)
- Optimal execution window calculation
- REST API with FastAPI
- Python library interface
- Basic test suite

### Known Limitations
- On-chain data fetching needs full implementation
- Basic heuristics (not ML-based)
- Limited false positive handling
- RPC rate limit constraints

