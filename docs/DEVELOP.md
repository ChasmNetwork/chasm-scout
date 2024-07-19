# Developing Chasm Scout

## Guideline

To start developing on Chasm Scout, follow these steps:

1. Fork the Repository: Click the "Fork" button on the top right of the repository page to create your own fork of the project.

2. Clone the Fork: Clone your fork to your local machine.

```sh
git clone https://github.com/your-username/chasm-scout.git
cd chasm-scout
```

3. Install dependencies:

   ```sh
   bun install
   ```

4. Set up the environment variables:

   ```sh
   cp .env.example .env
   ```

5. Start the development server:

   ```sh
   bun dev
   ```

6. Run/Add Tests: Ensure that all tests pass before making changes.

   ```sh
   bun run test
   ```

7. Make Your Changes: Develop new features, fix bugs, or improve documentation.

8. Commit Your Changes: Once you are satisfied with your changes, commit them to your fork.

   ```sh
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

9. Create a Pull Request: Go to the original repository and click on the "New Pull Request" button to create a new pull request from your fork.

## Docker Setup

To run the project using Docker, follow these steps:

1. Build the Docker image:

   ```sh
   docker build -t chasm-scout .
   ```

2. Run the Docker container:

   ```sh
   docker run -p 3000:3000 chasm-scout
   ```

3. Access the application at `http://localhost:3000`.

4. To stop the container, run:

   ```sh
   docker stop $(docker ps -a -q --filter ancestor=chasm-scout --format="{{.ID}}")
   ```

## Docker Compose Setup

To run the project using Docker Compose, follow these steps:

1. Build the Docker image:

   ```sh
   docker-compose build
   ```

2. Run the Docker container:

   ```sh
   docker-compose up
   ```

3. Access the application at `http://localhost:3000`.

4. To stop the container, run:

   ```sh
   docker-compose down
   ```

## Formatting & Linting

This project follows strict formatting and linting standards to ensure clean and consistent code across the codebase.

### Setting up VSCode

Step 1:
Install the [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) extension from Microsoft.

Step 2:
Open up `settings.json`

Step 3:
Add the following lines

```json
{
  "prettier.configPath": ".prettierrc.json",
  "editor.formatOnSave": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": ["typescript"],
  "eslint.codeActionsOnSave.mode": "problems"
}
```

### Prettier Setup

We utilize [Prettier](https://prettier.io/) for code formatting. Additionally, we have integrated the `@ianvs/prettier-plugin-sort-imports` plugin to sort import statements automatically.

To customize the import order, you can update the `importOrder` key in `.prettierrc.json` file as shown below:

```json
{
  "importOrder": ["<THIRD_PARTY_MODULES>", "", "^[./]"]
}
```

### Linting

For linting, we use ESLint, enforcing default recommended rules along with TypeScript-specific rules. ESLint is configured to only check for syntax issues and problems.

To configure additional rules, you can either use third-party plugins like Airbnb or define your own rules. Below are examples:

```javascript
// .eslintrc.json
{
  // Other configuration here
  rules: {
    // Custom rules here
  }
}
```

### Husky integration with lint-staged

We have set up Lint-Staged and Husky to run Prettier and ESLint on commit. This ensures that any formatting or linting issues are fixed automatically. If there are failures, the commit will be prevented.

### Github Workflows

GitHub Actions workflows have been configured to check formatting and linting on pull requests. Merging to the test, staging, and production environments will be blocked if there are any issues detected.
