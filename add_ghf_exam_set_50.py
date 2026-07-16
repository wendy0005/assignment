#!/usr/bin/env python3
"""Add 50 scenario-based GH-900 practice questions, safely and idempotently."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "progress.db"

# (domain index, question, options, correct option index, explanation)
QUESTIONS = [
    # Domain 1 — Introduction to Git and GitHub (9)
    (0, "A developer edits app.py, runs `git add app.py`, and then edits app.py again. What will the next commit contain if they commit immediately?", ["Both sets of edits", "Only the edits staged by `git add`", "Only the edits made after `git add`", "No edits until the file is staged twice"], 1, "Git commits the snapshot in the staging area. Later working-tree edits remain unstaged."),
    (0, "Your local branch has three commits that are not on GitHub. Which command publishes them to the configured remote branch?", ["git fetch", "git push", "git clone", "git status"], 1, "`git push` sends local commits and updates the remote branch reference."),
    (0, "A teammate wants to inspect changes from GitHub without merging them into the current branch. Which command should they use?", ["git pull", "git fetch", "git commit", "git restore"], 1, "`git fetch` downloads remote objects and references without merging them into the checked-out branch."),
    (0, "Why can every developer work while disconnected after cloning a Git repository?", ["GitHub caches every web page locally", "Each clone contains the repository history and a local object database", "Branches are stored only in the working directory", "Commits are queued in GitHub Actions"], 1, "Git is distributed: a normal clone contains the history needed for local commits, branches, and inspection."),
    (0, "You want Git to begin tracking a new file without creating a commit yet. What should you do?", ["Run `git add <file>`", "Run `git push <file>`", "Open a pull request", "Create a release"], 0, "`git add` places the file's current content in the staging area; committing is a separate step."),
    (0, "A commit was created on the wrong branch but must remain reachable while you switch branches. What is the safest first step?", ["Delete the `.git` directory", "Create a branch or tag pointing to the commit", "Run `git clean -fd`", "Remove the remote named origin"], 1, "A branch or tag preserves a reference to the commit so it is not left only in reflog history."),
    (0, "Which statement best distinguishes Git from GitHub?", ["Git is a distributed version control system; GitHub hosts Git repositories and collaboration features", "Git is a cloud service; GitHub is a local command", "Git tracks issues; GitHub tracks file versions", "They are two names for the same product"], 0, "Git manages version history; GitHub adds hosting, pull requests, issues, Actions, and other platform services."),
    (0, "After changing several files, you want to see which are staged, unstaged, or untracked. Which command gives that summary?", ["git status", "git blame", "git tag", "git remote"], 0, "`git status` summarizes the working tree and staging area relative to the current commit."),
    (0, "Two branches point to the same commit. What does creating another branch initially duplicate?", ["All repository files and history", "Only a lightweight reference to a commit", "The remote repository", "The `.gitignore` rules"], 1, "A Git branch is a lightweight movable reference, not a full copy of repository data."),

    # Domain 2 — Working with GitHub Repositories (9)
    (1, "A new contributor needs setup instructions and a project overview to appear on the repository front page. Which file is most appropriate?", ["README.md", "CODEOWNERS", "SECURITY.md", ".gitignore"], 0, "GitHub renders README files prominently and they commonly contain purpose, setup, and usage information."),
    (1, "A team wants pull requests that change `/docs/` to automatically request the documentation team. Which file should they configure?", ["CONTRIBUTING.md", "CODEOWNERS", "LICENSE", "CITATION.cff"], 1, "CODEOWNERS maps path patterns to users or teams and can trigger review requests."),
    (1, "A repository contains generated build output that should stay local. What should be added?", ["A matching pattern in `.gitignore`", "A label named generated", "A branch protection rule", "A wiki page"], 0, "`.gitignore` patterns keep untracked generated files from being added accidentally."),
    (1, "You lack write access to an open-source repository but want to propose a change. What is the standard workflow?", ["Fork it, create a branch in the fork, and open a pull request", "Create a milestone in the upstream repository", "Request the owner's password", "Upload a ZIP file to Discussions"], 0, "A fork provides a writable copy from which you can propose changes to the upstream project."),
    (1, "A maintainer wants others to know the legal terms for using and distributing the project. Which repository file provides them?", ["LICENSE", "README.md", "CODEOWNERS", "SUPPORT.md"], 0, "A license states the permissions and conditions governing use and distribution."),
    (1, "Which repository visibility allows access only to explicitly authorized users and teams?", ["Public", "Private", "Unlisted", "Archived"], 1, "Private repositories are restricted to granted users, teams, and apps."),
    (1, "A user wants a complete local working copy of an existing GitHub repository for the first time. Which operation should they use?", ["Clone", "Commit", "Merge", "Revert"], 0, "Cloning creates a local repository, working tree, history, and remote configuration."),
    (1, "A repository is archived. Which behavior should collaborators expect?", ["It becomes read-only for normal repository activity", "Its history is permanently deleted", "All forks are merged back", "It becomes a GitHub Pages site"], 0, "Archiving preserves the repository while making it read-only until an administrator unarchives it."),
    (1, "Where should maintainers document the expected process for proposing changes and running tests?", ["CONTRIBUTING.md", ".gitattributes", "CODEOWNERS", "LICENSE"], 0, "CONTRIBUTING.md explains contribution workflows, standards, and validation steps."),

    # Domain 3 — Collaboration Features (14)
    (2, "A pull request is not ready for final review, but the author wants early feedback and automated checks. What should they create?", ["A draft pull request", "A release", "A protected tag", "A private gist"], 0, "Draft pull requests support discussion and checks while clearly signaling that the work is not ready to merge."),
    (2, "A reviewer believes a pull request must be corrected before merge. Which review outcome communicates this?", ["Approve", "Comment", "Request changes", "Close issue"], 2, "Request changes records a blocking review when branch rules require approving reviews."),
    (2, "A pull request should automatically close issue 42 when merged. Which text in its description accomplishes this?", ["See #42", "Closes #42", "Related: 42", "Assign #42"], 1, "A supported closing keyword followed by the issue reference links and closes the issue when the PR merges."),
    (2, "Two contributors changed the same lines differently and GitHub reports a merge conflict. What must happen before merging?", ["Resolve the conflicting content and commit the resolution", "Add another label", "Convert the PR to a discussion", "Archive the base branch"], 0, "The competing changes must be reconciled into one valid version and committed."),
    (2, "A team wants all commits from a pull request represented by one new commit on the base branch. Which merge method fits?", ["Create a merge commit", "Squash and merge", "Rebase and merge", "Fast-forward only"], 1, "Squash and merge combines the pull request's changes into a single commit."),
    (2, "A reviewer has a suggestion that is optional and should not block merging. Which review outcome is most suitable?", ["Comment", "Request changes", "Delete branch", "Lock conversation"], 0, "A comment-only review gives feedback without approving or formally requesting changes."),
    (2, "A maintainer wants to discuss a broad product idea before defining actionable work. Which GitHub feature is best suited?", ["Discussions", "Releases", "Deploy keys", "Commit status"], 0, "Discussions support open-ended community conversation; accepted work can later become an issue."),
    (2, "An issue becomes heated and off-topic after the answer is final. What can a maintainer do to prevent more replies while preserving the record?", ["Lock the conversation", "Delete the repository", "Squash the issue", "Detach the fork"], 0, "Locking preserves existing content while restricting new comments."),
    (2, "A pull request shows a failing required status check. What is the expected result under branch protection?", ["It cannot merge until the required check passes or the rule is bypassed by an authorized actor", "It merges and reruns afterward", "It automatically becomes an issue", "It deletes the head branch"], 0, "Required status checks enforce successful validation before protected-branch updates."),
    (2, "What does the Files changed tab of a pull request primarily show?", ["The diff between the head and base branches", "Only files created on the default branch", "Organization billing changes", "The contributor's local staging area"], 0, "The tab presents the proposed additions, deletions, and modifications for review."),
    (2, "A reviewer writes a line-level note but has not submitted the review. Who can normally see the pending review comment?", ["Only the reviewer until the review is submitted", "Every GitHub user immediately", "Only organization owners", "Nobody, including the reviewer"], 0, "Pending review comments are held as part of the review until it is submitted."),
    (2, "After new commits invalidate an approval, the team wants another review automatically. Which protection setting helps?", ["Dismiss stale pull request approvals when new commits are pushed", "Allow force pushes", "Require linear history", "Automatically delete head branches"], 0, "Dismissing stale approvals ensures reviews apply to the current proposed changes."),
    (2, "A contributor wants to propose changing only one line directly from GitHub's web interface. What normally happens after editing?", ["They commit to a chosen branch and can open a pull request", "GitHub modifies every clone automatically", "The repository is archived", "A release is published"], 0, "Web edits are committed to a branch, after which the contributor can propose them through a PR."),
    (2, "A maintainer closes an unmerged pull request. What happens to its commits?", ["They remain on the head branch unless that branch is deleted", "They are added to the base branch", "They are removed from every clone", "They become release assets"], 0, "Closing a PR does not merge it or inherently delete its branch and commits."),

    # Domain 4 — Modern Development (6)
    (3, "A workflow must run whenever code is pushed to `main`. Where is this trigger declared?", ["In the workflow YAML under `on`", "In CODEOWNERS", "In the repository README", "In a milestone"], 0, "The `on` key in a `.github/workflows/*.yml` file defines events and filters."),
    (3, "A job needs Ubuntu and a clean execution environment supplied by GitHub. What should its workflow specify?", ["`runs-on: ubuntu-latest`", "`branch: ubuntu`", "`license: linux`", "`codespace: public`"], 0, "`runs-on` selects the runner environment used for the job."),
    (3, "A developer wants a cloud-hosted development environment configured from the repository. Which feature should they use?", ["GitHub Codespaces", "GitHub Sponsors", "GitHub Topics", "GitHub Releases"], 0, "Codespaces provides repository-based cloud development environments."),
    (3, "What is GitHub Copilot primarily designed to provide inside a supported editor?", ["AI-assisted code suggestions and chat help", "Repository billing reports", "Mandatory code approvals", "DNS hosting"], 0, "Copilot assists development with context-aware suggestions and conversational help."),
    (3, "A workflow needs a database password. What is the safest normal approach?", ["Store it as an Actions secret and reference the secret context", "Commit it in the workflow YAML", "Put it in README.md", "Add it as a public repository topic"], 0, "Actions secrets reduce accidental exposure and are referenced at runtime rather than committed."),
    (3, "A workflow contains build and deploy jobs; deploy must wait for build to succeed. Which job keyword expresses this dependency?", ["needs", "uses", "with", "name"], 0, "`needs` defines job dependencies and, by default, requires the dependency to succeed."),

    # Domain 5 — Project Management (3)
    (4, "A team wants a board, table, and roadmap using the same set of issues. Which feature should they use?", ["GitHub Projects", "Git tags", "Deployments", "Gists"], 0, "GitHub Projects supports multiple customizable views over issues, pull requests, and draft items."),
    (4, "Several issues must ship together in version 2.0 and the team wants completion progress. What should group them?", ["A milestone", "A fork", "A deploy key", "A code space"], 0, "Milestones group issues and pull requests around a goal and show progress toward completion."),
    (4, "The team wants to categorize issues as `bug`, `documentation`, or `priority: high`. Which feature should it use?", ["Labels", "Branches", "Releases", "Wikis"], 0, "Labels categorize and filter issues and pull requests."),

    # Domain 6 — Privacy, Security, and Administration (6)
    (5, "An account password is stolen, but the attacker lacks the user's second factor. Which control is providing protection?", ["Two-factor authentication", "A repository topic", "A milestone", "Git LFS"], 0, "2FA requires another proof beyond the password and substantially reduces account-takeover risk."),
    (5, "A contractor needs to triage issues but must not push code. Which principle should guide the permission granted?", ["Least privilege", "Public by default", "Shared credentials", "Force-push access"], 0, "Least privilege gives only the access needed for the assigned work."),
    (5, "GitHub detects that a committed token matches a known secret pattern. Which feature can alert maintainers?", ["Secret scanning", "GitHub Topics", "Milestones", "Wiki search"], 0, "Secret scanning detects supported credentials in repository content and history."),
    (5, "A dependency used by a project has a known vulnerable version. Which feature can notify the repository?", ["Dependabot alerts", "GitHub Sponsors", "Saved replies", "Traffic insights"], 0, "Dependabot alerts compare dependency data with known security advisories."),
    (5, "An organization wants members to access repositories through teams rather than many individual grants. What is the main benefit?", ["Centralized, role-based access management", "Automatic public visibility", "Unlimited Actions minutes", "Removal of repository history"], 0, "Teams make group permissions easier to assign, review, and update consistently."),
    (5, "A repository rule requires at least two approving reviews before changes reach `main`. What enforces this?", ["A protected branch or ruleset with required pull request reviews", "A README badge", "A discussion category", "A release note"], 0, "Branch protection and repository rulesets can require reviews before protected branches change."),

    # Domain 7 — Benefits of the GitHub Community (3)
    (6, "A developer wants to share a small reusable code snippet without creating a full repository. Which GitHub feature fits?", ["Gist", "Milestone", "Codespace", "Ruleset"], 0, "Gists are lightweight Git repositories designed for sharing snippets and small files."),
    (6, "A company reuses open-source collaboration practices across private internal repositories. What is this commonly called?", ["InnerSource", "Fork deletion", "Secret scanning", "Detached HEAD"], 0, "InnerSource applies open-source methods to software developed within an organization."),
    (6, "A maintainer wants recurring financial support for ongoing open-source work. Which GitHub program is designed for this?", ["GitHub Sponsors", "GitHub Issues", "GitHub Actions", "GitHub Pages"], 0, "GitHub Sponsors enables eligible developers and organizations to receive financial support."),
]


def main():
    if len(QUESTIONS) != 50:
        raise RuntimeError(f"Expected 50 questions, found {len(QUESTIONS)}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    existing = {row[0] for row in conn.execute(
        "SELECT question_text FROM quiz_questions WHERE course_id = 'ghf'"
    )}
    next_order = conn.execute(
        "SELECT COALESCE(MAX(sort_order), -1) + 1 FROM quiz_questions WHERE course_id = 'ghf'"
    ).fetchone()[0]

    added = 0
    for domain, question, options, answer, explanation in QUESTIONS:
        if question in existing:
            continue
        conn.execute(
            """INSERT INTO quiz_questions
               (course_id, chapter_idx, question_text, options_json, correct_idx, explanation, sort_order)
               VALUES ('ghf', ?, ?, ?, ?, ?, ?)""",
            (domain, question, json.dumps(options), answer, explanation, next_order),
        )
        next_order += 1
        added += 1

    conn.commit()
    total = conn.execute(
        "SELECT COUNT(*) FROM quiz_questions WHERE course_id = 'ghf'"
    ).fetchone()[0]
    conn.close()
    print(f"Added {added} questions; GitHub Foundations now has {total} questions.")


if __name__ == "__main__":
    main()
