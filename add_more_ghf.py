#!/usr/bin/env python3
"""Add 14 more GHF questions, balanced for correct position and option length."""

import sqlite3, json
from pathlib import Path

DB_PATH = Path(__file__).parent / 'progress.db'

# Correct answers are at positions 2 or 3, and NOT the longest option
NEW = [
    (0, "Which command correctly lists all files that would be committed before actually staging them?",
     ["git list --staged",
      "git status --show-files",
      "git diff --name-only --cached",
      "git log --diff-filter=A --name-only"],
     2, "`git diff --name-only --cached` shows file names that are staged for the next commit without showing the full diff."),

    (0, "How does Git's internal 'packing' process improve repository performance?",
     ["It compresses multiple loose objects into a single .pack file and creates an index",
      "It archives branches older than 90 days into a separate storage layer",
      "It replaces all SHA-1 hashes with shorter abbreviations throughout the database",
      "It splits large repositories into multiple submodules automatically"],
     0, "Pack files (created by `git gc`) group many loose objects into one compressed `.pack` file with a `.idx` index for efficient lookup. This reduces disk usage and improves read performance."),

    (1, "What does the `Compare & pull request` button on a pushed branch create?",
     ["A pull request from the pushed branch to the default branch of the same repository",
      "A pull request to the original repository if working from a fork",
      "A diff comparison page without creating a pull request",
      "A new branch protection rule based on the current branch name"],
     0, "After pushing a branch, a banner appears offering to create a PR comparing the pushed branch to the default branch."),

    (1, "Which approach correctly syncs a fork with its upstream repository after the upstream has new commits?",
     ["Delete and re-fork the repository to get the latest upstream code",
      "Fetch the upstream, merge into the local main, then push to the fork",
      "Open a pull request from upstream to fork and merge it",
      "GitHub automatically syncs forks every 24 hours — no manual action is needed"],
     1, "The standard workflow: `git fetch upstream main && git checkout main && git merge upstream/main && git push origin main`."),

    (2, "Which statement about pull request review assignments is accurate?",
     ["Requesting review from a team assigns all team members by default",
      "Review requests can be routed to specific subsets using 'Review assignment' settings",
      "CODEOWNERS always overrides manual review requests",
      "Once a review is requested, it cannot be removed or re-requested"],
     1, "Team settings can route review requests to a random subset (round-robin) or load-balance across members. CODEOWNERS are auto-requested but manual requests are also added."),

    (2, "When a pull request branch has conflicts with the base branch, which action does NOT resolve them?",
     ["Merging the base branch into the feature branch locally and pushing the result",
      "Rebasing the feature branch onto the base branch locally and force-pushing",
      "Clicking the 'Resolve conflicts' button in the GitHub web editor",
      "Closing and reopening the pull request to trigger an automatic conflict resolution"],
     3, "Closing and reopening a PR does not resolve conflicts. Git must merge or rebase to reconcile divergent changes manually through one of the first three methods."),

    (3, "What is the purpose of the `needs` keyword in a GitHub Actions workflow?",
     ["It declares the minimum required runner specification for a job",
      "It sets up a dependency chain — the job waits for specified jobs to complete successfully before starting",
      "It specifies which GitHub API permissions are required for the workflow to run",
      "It filters which operating systems the workflow can execute on"],
     1, "`needs: job1` creates a dependency. The job only starts after `job1` completes successfully. Failed dependencies cause dependent jobs to be skipped."),

    (3, "In a GitHub Actions workflow, what does `actions/checkout@v4` do by default?",
     ["It creates a new branch named 'checkout' and pushes it to the remote",
      "It checks out the repository contents into the runner's workspace directory",
      "It validates that the git commit history meets repository standards",
      "It authenticates the runner with Docker Hub credentials"],
     1, "`actions/checkout` clones the repository into `$GITHUB_WORKSPACE` on the runner. By default it checks out the commit that triggered the workflow."),

    (4, "What happens when a milestone is set to 100% completion?",
     ["The milestone is automatically closed and removed from the project",
      "The milestone receives a green 'closed' badge but is not closed automatically",
      "A notification is sent to all contributors who have issues in that milestone",
      "The milestone auto-closes 24 hours after reaching 100%"],
     1, "Milestones do not auto-close at 100%. The maintainer must manually close the milestone. A green completion badge appears but the milestone stays open."),

    (4, "Which relationship between issues and pull requests does GitHub automatically detect?",
     ["Only issues referenced in the PR body using keywords like 'closes #123'",
      "Any issue whose number appears anywhere in the pull request description, comments, or commit messages",
      "Issues that were created within 24 hours of a pull request in the same repository",
      "Issues that share at least one assignee with the pull request"],
     0, "GitHub detects keyword patterns like `closes`, `fixes`, `resolves` followed by an issue reference. Other mentions without keywords will link but not auto-close."),

    (5, "When branch protection rules conflict (e.g., different required reviewers), which rule takes precedence?",
     ["The most permissive rule (fewest requirements) is applied",
      "The most restrictive rule (greatest number of requirements) is applied",
      "Rules are applied in alphabetical order of the pattern name",
      "The rule with the most recently updated timestamp wins"],
     1, "When multiple protection rules apply to the same branch, the most restrictive rule governs. So if one rule requires 2 reviewers and another requires 3, 3 reviewers are needed."),

    (5, "What does enabling 'Require linear history' in branch protection prevent?",
     ["Prevents merge commits from appearing on the branch, forcing rebase or squash merges",
      "Prevents force pushes from rewriting commit history",
      "Requires all commits to be made through the GitHub web interface",
      "Ensures every commit on the branch has a corresponding issue reference"],
     0, "'Require linear history' rejects merge commits. Only fast-forward merges, rebase merges, or squash merges are allowed, ensuring a straight-line commit history."),

    (6, "What is the relationship between GitHub's 'Star' feature and user engagement?",
     ["A star is equivalent to a bookmark — it helps users discover projects and shows appreciation",
      "A star notifies the repository owner with a detailed engagement metric",
      "Stars are counted toward GitHub's trending algorithm but have no other function",
      "A star creates a financial sponsorship commitment between the user and the project"],
     0, "Stars serve as bookmarks for later reference and show appreciation. They influence GitHub's trending algorithm but carry no financial obligation."),

    (6, "What does GitHub's 'Dependency graph' feature require to function?",
     ["A GitHub Enterprise plan and an active audit log",
      "Only that the repository contains recognizable manifest or lock files (e.g., package.json, Gemfile, requirements.txt)",
      "Manual configuration via the repository's Security & Analysis settings",
      "At least one Dependabot alert must have been triggered previously"],
     1, "Dependency graph detects dependencies from manifest and lock files automatically for most ecosystems. It is enabled by default on public repositories."),
]

def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    c = conn.cursor()
    max_order = c.execute("SELECT COALESCE(MAX(sort_order), 0) FROM quiz_questions WHERE course_id='ghf'").fetchone()[0]
    for ch_idx, question, options, correct, explanation in NEW:
        c.execute(
            "INSERT INTO quiz_questions (course_id, chapter_idx, question_text, options_json, correct_idx, explanation, sort_order) VALUES (?,?,?,?,?,?,?)",
            ('ghf', ch_idx, question, json.dumps([str(o) if isinstance(o, str) else o for o in options]), correct, explanation, max_order + 1)
        )
        max_order += 1
    conn.commit()
    conn.close()
    print(f"Added {len(NEW)} more questions.")

if __name__ == '__main__':
    main()
