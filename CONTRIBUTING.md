# Contributing to Agent Workbench

Thank you for considering a contribution. Agent Workbench is a curated library of portable skills, agent role cards, templates, and small validation utilities. Contributions should make the collection more useful, understandable, safe, and maintainable.

## Before opening a pull request

1. Check the [skill catalog](SKILL_CATALOG.md), [source map](SOURCES.md), and existing folders to avoid duplicating a workflow.
2. Keep the change focused. Prefer one coherent improvement per pull request.
3. For a new skill, explain the specific situation that should activate it and the concrete output it should produce.
4. For changes informed by another project, verify the source and license, record the relationship in `sources.json`, and update `SOURCES.md` when needed. Do not copy upstream skill files, scripts, templates, or agent configurations into this repository.
5. Do not include credentials, API tokens, private data, personal information, local databases, generated build output, or unrelated files.

## Skill quality expectations

A skill should:

- use a directory name and frontmatter `name` that match as a lowercase hyphenated slug;
- include a concise, specific frontmatter `description` that says when the skill applies;
- provide actionable steps, necessary inputs, and a clear expected output;
- distinguish verified facts from assumptions and make important limitations explicit;
- avoid claiming that illustrative examples, mock data, or preview assets are evidence of live execution;
- stay focused on its own responsibility and avoid unnecessary overlap with existing skills.

Follow the structure and validation rules enforced by `scripts/validate_skills.py`. Update the catalog and source mapping when adding, renaming, or removing skills.

## Agent roles and templates

Keep role cards portable and explicit about their purpose, boundaries, and handoff. Templates should be practical, reusable starting points rather than project-specific filled-in records. Update the relevant README or catalog entry when adding a new role or template.

## Run the repository checks

The project uses Python's standard library for its local validation and test commands. From the repository root, run:

```bash
python scripts/validate_skills.py
python scripts/audit_skill_overlap.py
python -m unittest discover -s tests -v
```

Resolve failures introduced by your change before requesting a merge. The GitHub Actions quality workflow runs these same checks on pushes to `main` and on pull requests targeting `main`.

## Pull request checklist

- [ ] The change has a clear purpose and stays within the stated scope.
- [ ] Related catalog, source-map, and metadata files are updated.
- [ ] Attribution and license implications have been checked.
- [ ] The three repository checks pass locally.
- [ ] No secrets, private data, unrelated generated files, or unnecessary dependencies are included.
- [ ] Documentation describes limitations and demo-only behavior accurately.

Use a descriptive pull request title and summarize the motivation, changes, and verification performed. Link related issues where applicable.

## Reporting security concerns

Do not publish credentials, exploitable details, private user data, or sensitive examples in an issue or pull request. Use GitHub's private vulnerability reporting feature when it is enabled for the repository.

## Scope and review

By contributing, you confirm that you have the right to submit the material and that you have checked any applicable license terms. Maintainers may ask for changes that improve correctness, provenance, safety, clarity, or long-term maintainability.
