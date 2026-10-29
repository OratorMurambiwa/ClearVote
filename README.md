# ClearVote

Carnegie Young Leaders Fellowship 2026–2027 project to help identify political misinformation, AI-generated content, and deepfakes while promoting informed digital engagement.

## Getting Started

ClearVote is in early development. You can load the browser extension shell and run the backend text-preprocessing tests. The extension currently shows a placeholder popup and extracts up to 5,000 characters of page text locally, logging only the extracted length. A backend API server and the full claim-analysis flow are not implemented yet.

Clone the repository with Git and enter its root directory:

```bash
git clone https://github.com/OratorMurambiwa/ClearVote.git
cd ClearVote
```

Follow the component guides:

- [Browser extension setup and verification](extension/README.md) — requires Google Chrome; no build step or package installation.
- [Backend setup and tests](backend/README.md) — requires Python 3; uses the standard library only.

No API keys or environment variables are needed for these steps. The [Analyze API contract](docs/api-contract.md) describes the planned integration, and the [Milestone 2 checklist](docs/milestone-2.md) defines the intended end-to-end behavior.

## Contributing

### Finding Your Tasks

1. Open the **ClearVote** repository.
2. Go to **Projects → ClearVote Development → Board**.
3. Find the Issue assigned to you.
4. Read the Issue description and deliverables before starting.

### Workflow

For every assigned Issue:

1. Move the Issue from **To Do** to **In Progress** when you begin.
2. Open the Issue and go to the **Development** section.
3. Select **Create a branch** so the branch is linked to the Issue.
4. Create the branch from `main` using:

   `firstname-type-task`

   Example:

   `orator-research-apis`

5. Complete and test your work on that branch.
6. Commit your changes with clear commit messages.
7. Open a Pull Request into `main`.
8. In the PR description, add:

   `Closes #issue-number`

9. Move the Issue to **Review**.
10. Request at least one teammate as a reviewer.
11. Address any requested changes.
12. Merge only after approval. Once merged, the Issue should move to **Done**.

## Coding Standards

Use these conventions across the project:

- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `UPPER_CASE`
- One main class per file
- Class name should match the file name
- Keep files around **100–150 lines when practical**
- Add clear docstrings/documentation to functions and classes

## Important

- Do not work directly on `main`.
- Create a branch for each Issue.
- Keep your Issue status updated on the Project board.
