# Contributing to Sales & Inventory Forecasting System

Thank you for considering contributing to this project! Your help is essential for making this tool better.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- A clear, descriptive title
- Detailed description of the proposed feature
- Any relevant examples or mockups
- Explanation of why this feature would be useful

### Code Contributions

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Create a Pull Request

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Generate sample data:
   ```
   python src/generate_sample_data.py
   ```
4. Run tests:
   ```
   python -m unittest discover tests
   ```

## Code Style

Please follow these guidelines:
- Use PEP 8 style guide for Python code
- Write docstrings for all functions, classes, and modules
- Include comments for complex code sections
- Write meaningful commit messages

## Testing

- Add tests for new features
- Ensure all tests pass before submitting a pull request
- Aim for good test coverage

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
