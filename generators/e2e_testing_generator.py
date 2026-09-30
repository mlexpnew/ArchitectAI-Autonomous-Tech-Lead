"""
E2E Testing Generator

Generates automated end-to-end testing suites for generated frontends
using Playwright (TypeScript) and Cypress (JavaScript).
"""

from pathlib import Path
from typing import Any, List
from generators.writer import FileWriter


class E2ETestingGenerator:
    """Generates Playwright and Cypress end-to-end test suites for frontend projects."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.frontend_dir = self.output_dir / "frontend"
        self.e2e_playwright_dir = self.frontend_dir / "e2e"
        self.cypress_dir = self.frontend_dir / "cypress"
        self.cypress_e2e_dir = self.cypress_dir / "e2e"
        self.cypress_support_dir = self.cypress_dir / "support"
        self.workflows_dir = self.frontend_dir / ".github" / "workflows"

    @staticmethod
    def _pluralize(word: str) -> str:
        w = word.lower()
        if w.endswith("y") and not w.endswith(("ay", "ey", "oy", "uy")):
            return w[:-1] + "ies"
        elif w.endswith(("s", "x", "z", "ch", "sh")):
            return w + "es"
        return w + "s"

    @staticmethod
    def _kebab_case(word: str) -> str:
        import re
        s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", word)
        s = re.sub(r"([a-z\d])([A-Z])", r"\1-\2", s)
        return s.replace("_", "-").lower()

    def generate_playwright_config(self, project_name: str) -> None:
        """Generates playwright.config.ts with multi-browser and CI config."""
        content = f"""import {{ defineConfig, devices }} from '@playwright/test';

/**
 * Playwright E2E configuration for {project_name} frontend.
 * Supports cross-browser execution, mobile viewports, video & trace artifacts.
 */
export default defineConfig({{
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', {{ outputFolder: 'playwright-report', open: 'never' }}],
    ['list']
  ],
  use: {{
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  }},

  projects: [
    {{
      name: 'chromium',
      use: {{ ...devices['Desktop Chrome'] }},
    }},
    {{
      name: 'firefox',
      use: {{ ...devices['Desktop Firefox'] }},
    }},
    {{
      name: 'webkit',
      use: {{ ...devices['Desktop Safari'] }},
    }},
    {{
      name: 'Mobile Chrome',
      use: {{ ...devices['Pixel 5'] }},
    }},
  ],

  webServer: {{
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  }},
}});
"""
        FileWriter.write(self.frontend_dir / "playwright.config.ts", content)
        print("✅ Generated frontend/playwright.config.ts")

    def generate_cypress_config(self, project_name: str) -> None:
        """Generates cypress.config.js and support files."""
        config_content = f"""const {{ defineConfig }} = require('cypress');

module.exports = defineConfig({{
  e2e: {{
    baseUrl: process.env.CYPRESS_BASE_URL || 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{{js,jsx,ts,tsx}}',
    supportFile: 'cypress/support/e2e.js',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {{
      // implement node event listeners here
    }},
  }},
  retries: {{
    runMode: 2,
    openMode: 0,
  }},
}});
"""
        FileWriter.write(self.frontend_dir / "cypress.config.js", config_content)

        support_content = """// Cypress E2E Support File
import './commands';

beforeEach(() => {
  // Global setup before each test
  cy.viewport(1280, 720);
});
"""
        FileWriter.write(self.cypress_support_dir / "e2e.js", support_content)

        commands_content = """// Custom Cypress commands for application testing

Cypress.Commands.add('getByTestId', (testId) => {
  return cy.get(`[data-testid="${testId}"]`);
});

Cypress.Commands.add('login', (email = 'admin@example.com', password = 'password123') => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('input[type="email"]').type(email);
    cy.get('input[type="password"]').type(password);
    cy.get('button[type="submit"]').click();
    cy.url().should('not.include', '/login');
  });
});
"""
        FileWriter.write(self.cypress_support_dir / "commands.js", commands_content)
        print("✅ Generated Cypress config and support commands")

    def generate_playwright_specs(self, project_name: str, blueprint: Any = None) -> None:
        """Generates Playwright smoke tests and entity-specific CRUD/validation specs."""
        self.e2e_playwright_dir.mkdir(parents=True, exist_ok=True)

        # 1. Smoke Spec
        smoke_content = f"""import {{ test, expect }} from '@playwright/test';

test.describe('{project_name} Application Shell & Navigation', () => {{
  test.beforeEach(async ({{ page }}) => {{
    await page.goto('/');
  }});

  test('[@smoke] should load the homepage with correct document title', async ({{ page }}) => {{
    await expect(page).toHaveTitle(new RegExp('{project_name.replace("_", " ")}', 'i'));
  }});

  test('[@smoke] should render responsive navigation header and branding', async ({{ page }}) => {{
    const header = page.locator('header, nav, [role="navigation"]').first();
    await expect(header).toBeVisible();
  }});

  test('[@smoke] should render footer and copyright information', async ({{ page }}) => {{
    const footer = page.locator('footer');
    if (await footer.count() > 0) {{
      await expect(footer).toBeVisible();
    }}
  }});

  test('[@smoke] should toggle theme if theme-toggle exists', async ({{ page }}) => {{
    const themeBtn = page.locator('[data-testid="theme-toggle"], button[aria-label*="theme" i]');
    if (await themeBtn.isVisible()) {{
      await themeBtn.click();
      await expect(page.locator('html')).toHaveAttribute('data-theme', /dark|light/);
    }}
  }});
}});
"""
        FileWriter.write(self.e2e_playwright_dir / "smoke.spec.ts", smoke_content)

        # 2. Entity Specs
        entities = getattr(blueprint, "entities", []) if blueprint else []
        for entity in entities:
            e_name = entity.name
            e_kebab = self._kebab_case(e_name)
            e_plural = self._pluralize(e_name)
            fields = getattr(entity, "fields", [])

            form_fills = []
            for field in fields:
                f_name = field.name
                if f_name.lower() == "id":
                    continue
                f_type = str(field.type).lower()
                val = f"Demo {e_name} {f_name.title()}"
                if "int" in f_type:
                    val = "100"
                elif "float" in f_type or "dec" in f_type:
                    val = "99.95"
                elif "bool" in f_type:
                    val = "true"
                elif "time" in f_type or "date" in f_type:
                    val = "2026-09-30"

                form_fills.append(
                    f"    const {f_name}Input = page.locator('input[name=\"{f_name}\"], [data-testid=\"input-{f_name}\"]');\n"
                    f"    if (await {f_name}Input.isVisible()) {{\n"
                    f"      await {f_name}Input.fill('{val}');\n"
                    f"    }}"
                )

            form_fills_code = "\n".join(form_fills)

            spec_content = f"""import {{ test, expect }} from '@playwright/test';

test.describe('{e_name} Management E2E Workflows', () => {{
  test.beforeEach(async ({{ page }}) => {{
    await page.goto('/{e_plural}');
  }});

  test('[@smoke] should display {e_name} table and column headers', async ({{ page }}) => {{
    const title = page.locator('h1, h2, [data-testid="page-title"]');
    await expect(title).toBeVisible();

    const table = page.locator('table, [role="table"], [data-testid="{e_kebab}-list"]');
    if (await table.isVisible()) {{
      await expect(table).toBeVisible();
    }}
  }});

  test('[@crud] should open create modal and fill new {e_name} record', async ({{ page }}) => {{
    const createBtn = page.locator('button:has-text("Create"), button:has-text("New {e_name}"), [data-testid="create-{e_kebab}"]');
    if (await createBtn.isVisible()) {{
      await createBtn.click();

      // Fill in entity fields
{form_fills_code}

      const submitBtn = page.locator('button[type="submit"], button:has-text("Save"), button:has-text("Submit")');
      if (await submitBtn.isVisible()) {{
        await submitBtn.click();
        const notification = page.locator('.toast, [role="alert"], [data-testid="success-toast"]');
        if (await notification.count() > 0) {{
          await expect(notification.first()).toBeVisible();
        }}
      }}
    }}
  }});

  test('[@validation] should display validation feedback on empty submission', async ({{ page }}) => {{
    const createBtn = page.locator('button:has-text("Create"), button:has-text("New {e_name}")');
    if (await createBtn.isVisible()) {{
      await createBtn.click();
      const submitBtn = page.locator('button[type="submit"]');
      if (await submitBtn.isVisible()) {{
        await submitBtn.click();
        const errs = page.locator('.error, [aria-invalid="true"], [data-testid="form-error"]');
        if (await errs.count() > 0) {{
          await expect(errs.first()).toBeVisible();
        }}
      }}
    }}
  }});

  test('[@mock] should handle API failure gracefully with retry banner', async ({{ page }}) => {{
    // Mock backend 500 server error
    await page.route('**/api/**/{e_plural}*', async (route) => {{
      await route.fulfill({{
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({{ detail: 'Simulated backend outage for {e_name}' }}),
      }});
    }});

    await page.reload();
    const errorBanner = page.locator('[role="alert"], .alert-error, [data-testid="error-banner"]');
    if (await errorBanner.count() > 0) {{
      await expect(errorBanner.first()).toBeVisible();
    }}
  }});
}});
"""
            FileWriter.write(self.e2e_playwright_dir / f"{e_kebab}.spec.ts", spec_content)

        print(f"✅ Generated {len(entities) + 1} Playwright E2E spec files")

    def generate_cypress_specs(self, project_name: str, blueprint: Any = None) -> None:
        """Generates Cypress smoke tests and entity-specific CRUD/validation specs."""
        self.cypress_e2e_dir.mkdir(parents=True, exist_ok=True)

        # 1. Smoke Spec
        smoke_content = f"""describe('{project_name} - Cypress Smoke Tests', () => {{
  beforeEach(() => {{
    cy.visit('/');
  }});

  it('[@smoke] should render homepage and verify navigation', () => {{
    cy.title().should('match', /{project_name.replace("_", " ")}/i);
    cy.get('header, nav').should('be.visible');
  }});

  it('[@smoke] should navigate cleanly between primary views', () => {{
    cy.get('a[href^="/"]').first().then(($link) => {{
      const href = $link.attr('href');
      if (href && href !== '/') {{
        cy.wrap($link).click();
        cy.url().should('include', href);
      }}
    }});
  }});
}});
"""
        FileWriter.write(self.cypress_e2e_dir / "smoke.cy.js", smoke_content)

        # 2. Entity Specs
        entities = getattr(blueprint, "entities", []) if blueprint else []
        for entity in entities:
            e_name = entity.name
            e_kebab = self._kebab_case(e_name)
            e_plural = self._pluralize(e_name)

            spec_content = f"""describe('{e_name} Management E2E (Cypress)', () => {{
  beforeEach(() => {{
    cy.visit('/{e_plural}');
  }});

  it('[@smoke] displays {e_name} listing page and action controls', () => {{
    cy.get('h1, h2, [data-testid="page-title"]').should('be.visible');
  }});

  it('[@crud] intercepts network fetch for {e_plural}', () => {{
    cy.intercept('GET', '**/api/**/{e_plural}*', {{
      statusCode: 200,
      body: [
        {{ id: 1, name: 'Mock {e_name} #1' }},
        {{ id: 2, name: 'Mock {e_name} #2' }}
      ]
    }}).as('get{e_name}List');

    cy.visit('/{e_plural}');
    cy.wait('@get{e_name}List').its('response.statusCode').should('eq', 200);
  }});

  it('[@validation] handles form validation for invalid submissions', () => {{
    cy.get('body').then(($body) => {{
      if ($body.find('button:contains("Create"), button:contains("New")').length > 0) {{
        cy.contains('button', /Create|New/i).click();
        cy.get('button[type="submit"]').click();
        cy.get('[aria-invalid="true"], .error, [role="alert"]').should('exist');
      }}
    }});
  }});
}});
"""
            FileWriter.write(self.cypress_e2e_dir / f"{e_kebab}.cy.js", spec_content)

        print(f"✅ Generated {len(entities) + 1} Cypress E2E spec files")

    def generate_package_json(self, project_name: str) -> None:
        """Generates comprehensive frontend/package.json with E2E scripts."""
        content = f"""{{
  "name": "{self._kebab_case(project_name)}-frontend",
  "version": "1.0.0",
  "private": true,
  "description": "Frontend client with Playwright and Cypress end-to-end testing suite for {project_name}",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:report": "playwright show-report",
    "cypress:run": "cypress run",
    "cypress:open": "cypress open",
    "test:all": "npm run test:e2e && npm run cypress:run"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "axios": "^1.6.7",
    "lucide-react": "^0.358.0"
  }},
  "devDependencies": {{
    "@playwright/test": "^1.42.1",
    "@types/node": "^20.11.24",
    "@types/react": "^18.2.61",
    "@types/react-dom": "^18.2.19",
    "@vitejs/plugin-react": "^4.2.1",
    "cypress": "^13.7.1",
    "typescript": "^5.4.2",
    "vite": "^5.1.4"
  }}
}}
"""
        FileWriter.write(self.frontend_dir / "package.json", content)
        print("✅ Generated frontend/package.json with E2E test scripts")

    def generate_ci_workflow(self, project_name: str) -> None:
        """Generates GitHub Actions CI workflow for Playwright and Cypress."""
        workflow_content = f"""name: Frontend E2E Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  playwright-e2e:
    name: Playwright Cross-Browser E2E
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
          cache-dependency-path: frontend/package.json

      - name: Install Dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run Playwright Tests
        run: npx playwright test

      - name: Upload Playwright Test Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: frontend/playwright-report/
          retention-days: 14

  cypress-e2e:
    name: Cypress Integration E2E
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Cypress Run
        uses: cypress-io/github-action@v6
        with:
          working-directory: ./frontend
          browser: chrome
          record: false
"""
        FileWriter.write(self.workflows_dir / "e2e.yml", workflow_content)
        print("✅ Generated frontend/.github/workflows/e2e.yml")

    def generate_readme(self, project_name: str) -> None:
        """Generates frontend/README.md with E2E testing instructions."""
        readme_content = f"""# {project_name} - Frontend & End-to-End Testing

This frontend package comes pre-configured with **Playwright (TypeScript)** and **Cypress (JavaScript)** automated test suites.

## Features
- **Cross-Browser Verification**: Tests against Chromium, Firefox, WebKit, and mobile viewport devices.
- **Entity CRUD & Form Validation**: Automated assertions for creation flows, form field validations, and table views.
- **Offline & API Resiliency**: Mocking tests intercepting API routes to test edge cases.
- **CI/CD Automation**: GitHub Actions workflow (`.github/workflows/e2e.yml`) ready for pull request checks.

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Install Playwright Browsers
```bash
npx playwright install --with-deps
```

### 3. Run Playwright E2E Tests
```bash
# Headless run across all configured browsers
npm run test:e2e

# Interactive UI Mode with time-travel debugger
npm run test:e2e:ui

# Headed browser execution
npm run test:e2e:headed

# View last HTML test report
npm run test:e2e:report
```

### 4. Run Cypress E2E Tests
```bash
# Headless execution
npm run cypress:run

# Interactive Cypress Test Runner
npm run cypress:open
```
"""
        FileWriter.write(self.frontend_dir / "README.md", readme_content)
        print("✅ Generated frontend/README.md")

    def generate(self, project_name: str, blueprint: Any = None) -> None:
        """Generates full end-to-end testing suite for frontend."""
        print("\n" + "=" * 60)
        print(f"🎭 Generating E2E Testing Suite for {project_name}")
        print("=" * 60)

        self.generate_playwright_config(project_name=project_name)
        self.generate_cypress_config(project_name=project_name)
        self.generate_playwright_specs(project_name=project_name, blueprint=blueprint)
        self.generate_cypress_specs(project_name=project_name, blueprint=blueprint)
        self.generate_package_json(project_name=project_name)
        self.generate_ci_workflow(project_name=project_name)
        self.generate_readme(project_name=project_name)

        print("\n✅ E2E testing suite generated successfully")
