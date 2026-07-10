#!/usr/bin/env python3
"""Add 70 new harder questions to the GitHub Foundations quiz."""

import sqlite3, json
from pathlib import Path

DB_PATH = Path(__file__).parent / 'progress.db'

# Each question: (chapter_idx, question, [options], correct_idx, explanation)
NEW_QUESTIONS = [
    # ── Domain 0: Introduction to Git and GitHub ──
    (0, "What happens when you run `git commit --amend` without staging new changes?",
     ["It creates a new commit with an empty message",
      "It replaces the most recent commit with a new commit that has the same snapshot",
      "It deletes the most recent commit and resets the working directory",
      "It opens the editor to change the commit message of the previous commit"],
     3, "`git commit --amend` with staged changes replaces both the message and snapshot. Without staged changes, it only opens the editor to modify the commit message."),

    (0, "Which of the following is true about the Git object model?",
     ["A blob stores file content and the file name",
      "A tree stores directory structure and references to blobs or other trees",
      "A commit directly references blobs without using trees",
      "Annotated tags are stored as lightweight references in .git/refs/tags/"],
     1, "A tree object records the mapping between file names and blob objects (or nested trees). A blob stores only content, not the filename. A commit references a tree, not directly blobs."),

    (0, "What is the purpose of `git fetch` compared to `git pull`?",
     ["git fetch downloads changes and automatically merges them into the current branch",
      "git pull downloads changes but does not update any local branches",
      "git fetch downloads remote commits without updating the working directory or current branch",
      "git fetch is used only for tags, never for branches"],
     2, "`git fetch` downloads commits, objects, and refs from the remote without merging. `git pull` is `git fetch` + `git merge`."),

    (0, "Which command shows the difference between your local staging area and the last commit?",
     ["git diff",
      "git diff --cached",
      "git diff HEAD",
      "git log --patch"],
     1, "`git diff --cached` (or `git diff --staged`) shows changes staged for the next commit vs the last commit. Plain `git diff` shows unstaged changes vs the staging area."),

    (0, "In Git, what is a detached HEAD state?",
     ["When HEAD points to a branch that has been deleted remotely",
      "When HEAD points directly to a commit instead of a branch reference",
      "When the repository is in a merge conflict state",
      "When the working directory has uncommitted changes that prevent branch switching"],
     1, "A detached HEAD means HEAD points directly to a commit hash rather than a branch. Any commits made in this state can be lost when switching branches unless a new branch is created first."),

    (0, "What does the `--ff-only` flag do when merging?",
     ["It forces a merge commit even when a fast-forward is possible",
      "It only allows the merge if a three-way merge is required",
      "It aborts the merge if a fast-forward is not possible",
      "It skips the fast-forward and performs a rebase instead"],
     2, "`--ff-only` rejects the merge outright if a fast-forward isn't possible. It is useful for linear history workflows where merge commits are avoided."),

    (0, "What is stored in `.git/objects/` in a Git repository?",
     ["Only the commit history as plain text files",
      "All Git objects (blobs, trees, commits, tags) compressed and keyed by SHA-1 hash",
      "Configuration files and hook scripts for the repository",
      "A backup of all remote branches last fetched"],
     1, "`.git/objects/` stores all Git objects — blobs, trees, commits, and annotated tags — each compressed and identified by its SHA-1 hash. The first two characters form the subdirectory, the remaining 38 form the filename."),

    # ── Domain 1: Working with GitHub Repositories ──
    (1, "Which file format does GitHub use for rendering repository metrics such as contributor activity and commit frequency?",
     ["YAML",
      "Insights graphs are generated server-side and cannot be exported as a file format",
      "SVG",
      "CSV with a weekly cadence"],
     1, "Insights graphs (pulse, contributors, commit frequency, code frequency) are rendered server-side on github.com and are not stored as files in the repository."),

    (1, "What does the `--depth` option do in `git clone --depth 1`?",
     ["It clones only the first commit of each branch, creating a shallow copy",
      "It limits the cloning to repositories smaller than 1 GB",
      "It clones only files at depth 1 — the root directory",
      "It sets the maximum number of branches to clone to 1"],
     0, "`--depth 1` creates a shallow clone containing only the most recent commit. This is useful for CI/CD pipelines where full history isn't needed."),

    (1, "How can you rename the default branch from 'master' to 'main' in a GitHub repository?",
     ["Go to Settings → Branches → Default branch → rename it; then update local refs with `git branch -m`",
      "Delete the repository and create a new one with 'main' as default",
      "Run `git branch -M main` locally and push; GitHub automatically detects the new default",
      "Use the GitHub CLI command `gh repo edit --default-branch main` which handles everything"],
     0, "Steps: (1) Change default branch name in repo Settings → Branches. (2) Locally run `git branch -m master main` and `git fetch origin` then point to the new remote tracking branch."),

    (1, "What happens when you push a tag to GitHub that has the same name as an existing branch?",
     ["The tag overwrites the branch",
      "GitHub rejects the push with an error",
      "The tag and branch coexist but the tag takes precedence in checkout by reference name",
      "The tag is silently renamed with a `-tag` suffix"],
     1, "GitHub rejects the push because tag and branch names must be unique within a repository. The error message indicates the name already exists."),

    (1, "What is the purpose of `.gitkeep` in Git repositories?",
     ["It tells Git to keep a file even if it matches a .gitignore pattern",
      "Git tracks `.gitkeep` as a special sentinel that prevents garbage collection",
      "It is a convention — Git does not track empty directories, so a placeholder file forces the directory to exist",
      "It configures the repository to retain all commit history indefinitely"],
     2, "`.gitkeep` is a naming convention (not a Git feature) — an empty `.gitkeep` file is committed so that Git includes the otherwise-empty directory in the repository."),

    (1, "Which of the following is NOT possible through a GitHub repository's Settings tab?",
     ["Transferring repository ownership to another user or organization",
      "Setting branch protection rules for specific branches",
      "Changing the repository's license after creation",
      "Creating a personal access token"],
     3, "Personal access tokens are managed at the account level under Settings → Developer settings, not within an individual repository's settings."),

    (1, "What does `git worktree` allow you to do?",
     ["Visualize the branching tree structure of the repository",
      "Check out multiple branches simultaneously in separate working directories from the same repository",
      "Create a temporary copy of the repository for experimental changes",
      "Merge two different repositories into a single working tree"],
     1, "`git worktree add <path> <branch>` creates a new working directory where a different branch is checked out, allowing parallel work without stashing or cloning again."),

    # ── Domain 2: Collaboration Features ──
    (2, "What happens when two pull requests modify the same lines of code and the first one is merged?",
     ["The second PR is automatically updated and GitHub highlights the conflict",
      "The second PR is closed automatically",
      "GitHub merges both changes using a three-way merge",
      "The second PR's branch is deleted to prevent conflicts"],
     0, "GitHub detects the conflict on the second PR and displays a banner: 'This branch has conflicts that must be resolved'. The PR author or maintainer must resolve the conflict before merging."),

    (2, "What is the purpose of a pull request draft?",
     ["It creates a PR that can only be merged by organization owners",
      "It opens a PR that cannot be merged until it is marked as 'Ready for review'",
      "It hides the PR from everyone except the author",
      "It automatically assigns reviewers from the CODEOWNERS file"],
     1, "Draft PRs are visible to collaborators but cannot be merged. The author marks it 'Ready for review' when it's complete. This signals work-in-progress."),

    (2, "When you request a review from a team on a pull request, who is assigned?",
     ["Every member of the team",
      "A random member of the team selected by GitHub's load-balancing algorithm",
      "Only the team leads listed in the team settings",
      "The entire team and all sub-teams are assigned"],
     0, "When a team is requested for review, all members of that team are listed as reviewers. GitHub's review assignment can optionally auto-assign a subset if configured in team settings."),

    (2, "What is the difference between a fork and a branch in a collaborative workflow?",
     ["A fork creates a personal copy of the repository on your account; a branch is a divergent line of work within the same repository",
      "A branch is permanent; a fork is temporary",
      "A fork is used only for public repositories; a branch is used only for private repositories",
      "There is no practical difference — both allow isolated development"],
     0, "Forks copy the entire repo to your account (used when you lack write access). Branches are lightweight pointers within the same repo (requires write access)."),

    (2, "What does the 'Rebase and merge' option on a pull request do?",
     ["It creates a merge commit that combines all PR commits",
      "It applies each PR commit individually onto the base branch, rewriting history",
      "It squashes all PR commits into one and rebases it onto the base branch",
      "It discards the PR commits and creates an empty merge commit for review purposes"],
     1, "'Rebase and merge' takes each commit from the head branch and replays them onto the base branch individually, producing a linear history. No merge commit is created."),

    (2, "Which permission level is required for a user to add a pull request to a GitHub Project?",
     ["Write access to the repository",
      "Read access to the repository and access to the project",
      "Admin access to the repository",
      "Only organization owners can link PRs to projects"],
     0, "Write access to the repository is required to add PRs to a project. Read access lets you view projects but not add items."),

    (2, "What happens when you 'Close with comment' on a pull request without merging?",
     ["The PR branch is automatically deleted",
      "The PR is closed and no further commits can be pushed to the branch",
      "The PR is closed but the branch remains intact for future use",
      "All pending review requests are automatically approved"],
     2, "Closing a PR without merging keeps the branch intact. It can be reopened later or used as the basis for a new PR."),

    # ── Domain 3: Modern Development ──
    (3, "What is the purpose of a GitHub Actions self-hosted runner?",
     ["To run workflows on your own infrastructure instead of GitHub-hosted runners",
      "To host a local mirror of GitHub repositories for offline access",
      "To automatically scale GitHub Actions across multiple cloud providers",
      "To replace GitHub's workflow engine with a custom CI/CD pipeline"],
     0, "Self-hosted runners let you run workflows on machines you control, useful for accessing private network resources or specialized hardware."),

    (3, "In GitHub Actions, what does `on: pull_request_target` do differently from `on: pull_request`?",
     ["`pull_request_target` runs with the base branch context instead of the merge commit, allowing safe access to secrets",
      "`pull_request_target` triggers only when a PR targets the default branch",
      "`pull_request_target` blocks the workflow if the PR contains sensitive changes",
      "`pull_request_target` requires manual approval before the workflow can run"],
     0, "`pull_request_target` runs in the context of the base branch (not the merge commit), so secrets are available but the PR code isn't checked out unsafely. This is designed for labelers or commenters where checking out PR code is unnecessary."),

    (3, "What does the `GITHUB_TOKEN` secret provide in a GitHub Actions workflow?",
     ["An authentication token that expires after 60 minutes and has access limited to the current repository",
      "A permanent deployment key for accessing external APIs",
      "A token that grants admin access to all repositories in the organization",
      "A read-only token that can only clone public repositories"],
     0, "`GITHUB_TOKEN` is an automatically generated, repository-scoped token that expires when the workflow completes. It can push to the repo, create issues, and open PRs within the same repository."),

    (3, "What is the difference between `on: push` and `on: workflow_dispatch` in GitHub Actions?",
     ["`push` triggers on code pushes; `workflow_dispatch` allows manual triggering through the GitHub UI or API",
      "`push` triggers on all branches; `workflow_dispatch` triggers only on the default branch",
      "There is no difference — both trigger on code changes",
      "`push` requires a workflow file; `workflow_dispatch` does not"],
     0, "`workflow_dispatch` creates a manual trigger button in the Actions tab. It can accept input parameters. `push` triggers automatically on every push event."),

    (3, "In GitHub Actions, how can you conditionally run a step only on a specific branch?",
     ["Using the `if` keyword with `github.ref == 'refs/heads/main'`",
      "Using the `branches` filter in the `on:` trigger together with `if: contains(github.ref, 'main')`",
      "Wrapping the step in a `${{ if branch == 'main' }}` conditional block",
      "Using `on: push: branches: [main]` — which already limits the workflow to main"],
     0, "The `if` keyword evaluates a condition expression at runtime. `github.ref` contains the full reference string. The `branches` filter on `on: push` prevents the workflow from even running on other branches."),

    (3, "What does GitHub Copilot use as context to generate code suggestions?",
     ["Only the current file being edited",
      "The surrounding code context, open files, and the cursor position",
      "A separate AI training dataset that excludes the user's own code",
      "Only comments prefixed with `// copilot:` directives"],
     1, "Copilot uses the code in the active file, nearby open tabs, and the cursor context to generate relevant suggestions. It does not send prompts using comments alone."),

    (3, "What does the `matrix` strategy do in a GitHub Actions workflow?",
     ["It creates a dependency graph of all jobs in the workflow",
      "It runs a job multiple times with different combinations of variables (e.g., different OS or Node versions)",
      "It organizes workflow runs into a grid view for monitoring",
      "It distributes workflow steps across multiple runners in parallel"],
     1, "The `matrix` strategy defines a set of different configurations. The job runs once for each combination. For example, testing on `[ubuntu, macos]` × `[node14, node16]`."),

    # ── Domain 4: Project Management ──
    (4, "What is the difference between 'Milestone' and 'Project' in GitHub?",
     ["A Milestone groups issues by due date; a Project organizes issues as customizable views (table, board, roadmap)",
      "Milestones are for public repos only; Projects are for private repos only",
      "A Milestone tracks time; a Project tracks code reviews",
      "There is no difference — both are interchangeable tools for issue grouping"],
     0, "Milestones track progress toward a specific goal by due date. Projects are flexible view-based tools (table, board, timeline) for organizing issues, PRs, and notes."),

    (4, "When you convert an issue to a pull request, what happens to the issue?",
     ["The issue is automatically closed and linked to the new pull request",
      "The issue is deleted and replaced by the pull request",
      "The issue remains open and is automatically referenced in the pull request body",
      "The issue is converted to a pull request draft on a new branch"],
     2, "When you convert an issue to a PR, the issue stays open and is referenced in the PR body. Closing the PR does not close the issue automatically."),

    (4, "Which of the following is true about GitHub issue templates?",
     ["They are stored in `.github/ISSUE_TEMPLATE/` and can be configured with YAML frontmatter or markdown",
      "They can only be created by repository administrators",
      "They are stored in the repository's wiki, not the main repository",
      "They must be written exclusively in YAML format"],
     0, "Issue templates go in `.github/ISSUE_TEMPLATE/`. They can use YAML form definitions (`.yml`) with form elements or Markdown (`.md`) with a template body and YAML frontmatter."),

    (4, "What does the 'Tracked in Projects' badge on an issue indicate?",
     ["The issue has been added to at least one project board",
      "The issue is being tracked by a GitHub Actions workflow",
      "The issue has been assigned to a milestone with a due date",
      "The issue has been escalated to organization administrators"],
     0, "The 'Tracked in Projects' badge appears after adding an issue to a GitHub Project. It shows the project name and provides a quick link to the project item."),

    (4, "What happens to a project board card when the associated issue is closed?",
     ["The card is automatically removed from the project",
      "The card remains in its current column but receives a closed status indicator",
      "The card is moved to a 'Done' column if one exists, otherwise it stays put",
      "The card is archived and hidden from default project views"],
     2, "When an issue is closed, its project card moves to the 'Done' column if the project has one. If no 'Done' column exists, the card stays where it is."),

    # ── Domain 5: Privacy, Security, and Administration ──
    (5, "What is the difference between 'Dependency graph' and 'Dependabot alerts'?",
     ["Dependency graph identifies dependencies; Dependabot alerts notify about known vulnerabilities in those dependencies",
      "Dependency graph only works for npm packages; Dependabot alerts work for all ecosystems",
      "Both are the same feature with different names in different GitHub plans",
      "Dependency graph is public; Dependabot alerts are always private"],
     0, "Dependency graph scans your repository to build a list of dependencies. Dependabot alerts cross-reference this list against the GitHub Advisory Database to flag known vulnerabilities."),

    (5, "What does enabling 'Require signed commits' in a branch protection rule enforce?",
     ["All commits pushed to the protected branch must be GPG or S/MIME signed and verified",
      "Users must sign a terms-of-service agreement before pushing",
      "Commits must be made through the GitHub web interface only",
      "All contributors must have two-factor authentication enabled before committing"],
     0, "This setting rejects unsigned commits and unverified signatures on the protected branch. Commits must have a valid GPG or S/MIME signature that GitHub can verify."),

    (5, "What is the minimum permission required for a GitHub App to create issue comments via the API?",
     ["Read permissions for issues",
      "Write permissions for issues",
      "Write permissions for pull requests",
      "Administration permissions for the repository"],
     1, "To create or edit issue comments via the API, a GitHub App needs 'Issues: Write' permission. Read permission only allows viewing comments."),

    (5, "What happens when a repository is made private after being public?",
     ["Forks of the repository are automatically deleted",
      "Existing forks become hidden from the fork network but remain as standalone repos",
      "All forks are automatically converted to private as well",
      "Forks remain public and can continue to create pull requests to the original"],
     1, "When a public repo is made private, its forks are detached from the fork network. They remain as independent repositories but are no longer visible in the fork list."),

    (5, "What is the purpose of the `SECURITY.md` file in a GitHub repository?",
     ["To document the project's security policies, including how to responsibly report vulnerabilities",
      "To automatically configure GitHub's security features such as code scanning",
      "To list all known vulnerabilities in the project's dependencies",
      "To enforce two-factor authentication for all contributors"],
     0, "SECURITY.md tells users and security researchers how to report vulnerabilities responsibly. It typically includes contact methods, expected response times, and supported versions."),

    (5, "What does enabling 'Force push' restriction in a branch protection rule prevent?",
     ["It prevents anyone from rewriting history on the protected branch",
      "It only prevents force pushes from non-admin users",
      "It prevents force pushes except when using the 'Rebase and merge' option",
      "It blocks all pushes to the branch, including regular commits"],
     0, "When 'Restrict who can push to matching branches' is checked with 'Force push' restricted, no one — including admins — can force push to the protected branch."),

    (5, "What is the difference between a `personal access token` (PAT) and a `deploy key`?",
     ["A PAT authenticates as the user; a deploy key authenticates as a repository-level SSH key",
      "A PAT expires; a deploy key does not expire",
      "A PAT can access multiple repositories; a deploy key only grants access to a single repository",
      "All of the above"],
     3, "PATs act on behalf of a user across any repos the user can access (scoped by permissions). Deploy keys are SSH keys attached to a single repository for read or write access."),

    # ── Domain 6: Benefits of the GitHub Community ──
    (6, "What is the primary purpose of the GitHub Community Guidelines?",
     ["To define technical standards for repository structure and CI/CD configuration",
      "To establish expected behavior for respectful and constructive collaboration",
      "To list GitHub's pricing tiers and feature availability",
      "To specify file size limits and storage quotas for repositories"],
     1, "The Community Guidelines focus on behavior: being respectful, accepting feedback gracefully, and avoiding harassment. They apply to all interactions on GitHub."),

    (6, "What is measured by the 'Community Standards' section of a public repository's Community Profile?",
     ["The number of active contributors compared to a rolling 90-day average",
      "Key metrics such as README, contributing guidelines, license, issue templates, and code of conduct",
      "The percentage of issues resolved within 7 days",
      "The total number of stars and forks compared to similar repositories"],
     1, "The Community Profile checks for presence of: README, CONTRIBUTING.md, LICENSE, issue templates, PR templates, and a code of conduct. A passing score requires most of these."),

    (6, "Why does the GitHub community recommend having a CONTRIBUTING.md file?",
     ["It is required for all public repositories on GitHub",
      "It reduces maintainer workload by clearly documenting expectations for bug reports, features, and pull requests",
      "It automatically enables GitHub Issues and Pull Requests",
      "It improves the repository's search ranking on GitHub"],
     1, "CONTRIBUTING.md is optional but strongly recommended. It sets expectations, reducing low-quality issues and PRs that waste maintainer time."),

    (6, "What is the significance of the 'Code of Conduct' for open-source projects?",
     ["It is legally binding and enforceable in court",
      "It establishes a framework for acceptable behavior and helps maintain a welcoming community",
      "It defines the technical architecture and coding standards for contributions",
      "It lists all contributors and their roles within the project"],
     1, "A Code of Conduct sets behavioral expectations. Projects like Contributor Covenant provide templates. It helps maintainers address harassment and toxic behavior."),

    (6, "Which of the following is NOT a benefit of using GitHub Discussions?",
     ["Enabling Q&A with a marked-as-answer feature",
      "Replacing issues for tracking bugs and feature requests",
      "Allowing categorized conversations that can be searched and referenced",
      "Automatic conversion of popular discussions into issues"],
     3, "GitHub Discussions supports Q&A, announcements, and general conversation with categories. However, there is no automatic conversion of discussions to issues — it must be done manually."),

    (6, "What does the 'Sponsor' button on an open-source repository allow users to do?",
     ["Financially support the project through recurring or one-time payments via GitHub Sponsors",
      "Claim co-ownership of the repository by paying a sponsorship fee",
      "Request prioritized feature development in exchange for payment",
      "Receive a verified badge on their GitHub profile"],
     0, "GitHub Sponsors enables financial support for open-source contributors. It can be set up by individual accounts or organizations."),

    (6, "How does GitHub's 'Explore' feature help users discover new projects?",
     ["It curates trending repositories, topics, and collections tailored to the user's activity",
      "It shows repositories with the most open issues for contributors to find",
      "It lists all newly created repositories in chronological order",
      "It recommends repositories based on the user's LinkedIn connections"],
     0, "GitHub Explore shows trending repos, curated topics, and personalized recommendations based on followed users, starred repos, and contribution history."),
]

def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    c = conn.cursor()

    # Get max sort_order
    max_order = c.execute("SELECT COALESCE(MAX(sort_order), 0) FROM quiz_questions WHERE course_id='ghf'").fetchone()[0]

    added = 0
    for ch_idx, question, options, correct, explanation in NEW_QUESTIONS:
        c.execute(
            "INSERT INTO quiz_questions (course_id, chapter_idx, question_text, options_json, correct_idx, explanation, sort_order) VALUES (?,?,?,?,?,?,?)",
            ('ghf', ch_idx, question, json.dumps(options), correct, explanation, max_order + added + 1)
        )
        added += 1

    conn.commit()
    conn.close()
    print(f"Added {added} new questions to GitHub Foundations quiz.")

if __name__ == '__main__':
    main()
