# Contributing to pymenu-cli

Thank you for considering contributing to pymenu-cli! We welcome all contributions, whether they are bug reports, feature requests, or code improvements. Please take a moment to review this document before submitting your contributions.

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by [opening an issue](https://github.com/moraneus/pymenu-cli/issues). Include as much detail as possible to help us reproduce and fix the issue quickly. Make sure to include:

- A clear and descriptive title.
- A detailed description of the problem.
- Steps to reproduce the issue.
- Any relevant logs or screenshots.

### Suggesting Enhancements

We welcome suggestions for new features and enhancements. To suggest an enhancement, please [open an issue](https://github.com/moraneus/pymenu-cli/issues) and provide:

- A clear and descriptive title.
- A detailed description of the proposed enhancement.
- Any relevant examples or mockups.

### Submitting Pull Requests

To submit a pull request (PR), follow these steps:

1. **Fork the repository**: Click the "Fork" button at the top of this page to create a copy of the repository on your GitHub account.

2. **Clone your fork**: Clone the forked repository to your local machine using the following command:
    ```bash
    git clone https://github.com/moraneus/pymenu-cli.git
    cd pymenu-cli
    ```

3. **Create a new branch**: Create a new branch for your work. Use a descriptive name for the branch:
    ```bash
    git checkout -b feature/my-new-feature
    ```

4. **Make your changes**: Make your changes in the new branch.

5. **Commit your changes**: Commit your changes with a clear and concise commit message:
    ```bash
    git add .
    git commit -m "Add feature: my new feature"
    ```

6. **Push to your fork**: Push your changes to your forked repository:
    ```bash
    git push origin feature/my-new-feature
    ```

7. **Open a pull request**: Go to the original repository and open a pull request from your forked repository. Provide a clear and descriptive title and description for your PR.

### Code Style and Guidelines

- Follow the existing code style and conventions.
- Write clear and concise commit messages.
- Write tests for new features and bug fixes.
- Ensure your code passes all existing tests.

### Running Tests

Before submitting your PR, make sure all tests pass. You can run the tests using the following commands:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
