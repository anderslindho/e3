import pprint
from typing import NoReturn

import gitlab
from gitlab.v4.objects import Project


def protect_branch(
    project: Project = None,
    branch: str = None,
    allowed_to_push: int = gitlab.DEVELOPER_ACCESS,
    allowed_to_merge: int = gitlab.DEVELOPER_ACCESS,
    simulate: bool = True,
) -> NoReturn:
    """Protects branch.

    :param project: affected gitlab project/repository
    :param branch: branch name or wildcard
    :param allowed_to_push: minimum gitlab access level required to push
    :param allowed_to_merge: minimum gitlab access level required to merge
    :param simulate: dry-run option
    """
    if project is None or branch is None:
        raise ValueError

    if simulate:
        print(f"Branch '{branch}' of {project.name} would have been protected")
    else:
        try:
            project.protectedbranches.delete(branch)
        except gitlab.exceptions.GitlabDeleteError:
            pass
        else:
            print(f"Existing protected '{branch}' in {project.name} unprotected")
        finally:
            print(f"Protecting the branch '{branch}'")
            p_branch = project.protectedbranches.create(
                {
                    "name": branch,
                    "allowed_to_push": [{"access_level": allowed_to_push}],
                    "allowed_to_merge": [{"access_level": allowed_to_merge}],
                }
            )
            print("Protected branch:", pprint.pformat(vars(p_branch)))


def protect_tag(
    project: Project = None, tag: str = None, simulate: bool = True
) -> NoReturn:
    """Protects tag.

    :param project: affected gitlab project/repository
    :param tag: tag name or wildcard
    :param simulate: dry-run option
    """
    if project is None or tag is None:
        raise ValueError

    if simulate:
        print(f"Tag '{tag}'' of {project.name} would have been protected")
    else:
        try:
            project.protectedtags.delete(tag)
        except gitlab.exceptions.GitlabDeleteError:
            pass
        else:
            print(f"Existing protected tag '{tag}' in {project.name} unprotected")
        finally:
            print(f"Protecting the tag '{tag}'")
            p_tag = project.protectedtags.create(
                {
                    "name": tag,
                }
            )
            print("Protected tag:", pprint.pformat(vars(p_tag)))
