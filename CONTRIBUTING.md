# Contributing to Cross-Cloud SOC Auto-Remediation System

Thank you for your interest in contributing! This project aims to provide a production-grade security automation reference architecture.

## How to Contribute

### 1. Report Bugs
- Use GitHub Issues
- Include: environment details, steps to reproduce, expected vs actual behavior
- Mark with `bug` label

### 2. Suggest Enhancements
- Use GitHub Issues
- Include: use case, proposed solution, alternatives considered
- Mark with `enhancement` label

### 3. Submit Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/cross-cloud-soc-auto-remediation.git
cd cross-cloud-soc-auto-remediation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r lambda/requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Run tests
cd lambda
pytest tests/ -v --cov=src