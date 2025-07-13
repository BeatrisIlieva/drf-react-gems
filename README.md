# django-ts-gems

## Recommended Editor Extensions

For the best development experience, we recommend installing the following extensions in your code editor (especially if you use VSCode):

### VSCode Extensions
- **Python** (`ms-python.python`)
- **Django** (`batisteo.vscode-django`)
- **Pytest Test Adapter** (`littlefoxteam.vscode-python-test-adapter`)
- **Pylance** (`ms-python.vscode-pylance`) for fast, feature-rich Python language support

These extensions provide:
- Syntax highlighting and code completion for Python and Django
- Inline linting and error checking
- Test discovery and running from the UI
- Code navigation and refactoring tools

**Note:**
- These extensions are optional. All tests and coverage commands will still work from the terminal even if you do not have them installed.
- If you use another editor (like PyCharm), make sure to enable Python and Django support for similar benefits.

---

## Test Coverage: Generating and Viewing Reports

This project uses [coverage.py](https://coverage.readthedocs.io/) to measure and report test coverage for the Django/DRF backend.

### How to Run Tests and Generate Coverage Reports

1. **Run tests:**

   From the `server/` directory, run:

   ```sh
   python manage.py test
   ```

2. **Run tests with coverage:**

   From the `server/` directory, run:

   ```sh
   coverage run manage.py test
   coverage report
   coverage html
   ```

3. **View the HTML report:**

   After running the commands above, open the following file in your browser:

   ```
   server/htmlcov/index.html
   ```

   This gives you a detailed, navigable report showing which lines are covered by tests.

### Keeping Coverage Reports Out of Version Control & Deployment

- Coverage artifacts (`htmlcov/`, `.coverage`, `coverage.xml`) are **excluded from git** via `server/.gitignore`.
- This ensures reports are never committed or deployed.
- Each developer or CI run can generate and view their own reports.

---

For questions, see the [coverage.py documentation](https://coverage.readthedocs.io/) for configuration and usage details.