from pathlib import Path

from gitgud import operations
from gitgud.user_messages import display_tree_content, separated, existence_str


@separated
def repo_already_initialized():
    file_operator = operations.get_operator()
    print('Repo {} already initialized for Git Gud.'
          .format(file_operator.path))
    print('Use --force to initialize {}.'.format(Path.cwd()))
    if file_operator.path != Path.cwd():
        print('{} will be left as is.'.format(file_operator.gg_path))  # noqa: E501


def target_branch_str():
    file_operator = operations.get_operator()
    referred_by = file_operator.get_branches_by_commit()
    for target in referred_by:
        referred_by[target] = ", ".join(referred_by[target])
    return referred_by


def display_commit_content(show_branches=True, show_content=True, sort_commits=True, num_files=2, num_commits=2):  # noqa: E501
    file_operator = operations.get_operator()
    referred_by = target_branch_str()

    commit_format_str = '"{message}"'
    if show_branches:
        commit_format_str += "{branches}"

    commits = file_operator.get_all_commits(sort_commits)
    for commit in commits:
        if commit.hexsha in referred_by and show_branches:
            branches = f" ({referred_by[commit.hexsha]})"
        else:
            branches = ""
        header = commit_format_str.format(
            message=commit.message.split('\n')[0].strip(),
            branches=branches
        )
        display_tree_content(
            header,
            file_operator.get_commit_content(commit),
            show_content=show_content,
            num_files=num_files
        )

    for commit_num in range(len(commits), num_commits):
        print(f"Commit {commit_num+1}: " + existence_str(False))

def display_working_directory_content(**kwargs):
    file_operator = operations.get_operator()
    working_dir = file_operator.get_working_directory_content()
    display_tree_content("Working Directory", working_dir, **kwargs)


def display_staging_area_content(**kwargs):
    file_operator = operations.get_operator()
    staging_area = file_operator.get_staging_content()
    display_tree_content("Staging Area", staging_area, **kwargs)


def display_repo_files():
    display_working_directory_content(show_content=False)
    display_staging_area_content(show_content=False)
    print()
    print("Commits:")
    display_commit_content(show_branches=False, show_content=False)
