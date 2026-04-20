"""
Purpose:
    Centralize role and scope checks for organization and admin endpoints.
Inputs:
    Authenticated principal context from JWT dependencies.
Outputs:
    Small helper functions used by routes and tests.
Dependencies:
    Route-level principal dictionaries and role constants.
TODO Checklist:
    - [ ] Replace simple string checks with DB-backed membership permissions.
    - [ ] Add per-workspace scoped roles once workspace selection is real.
    - [ ] Add publish/review policy helpers when governance rules are finalized.
"""

from collections.abc import Iterable


ORG_ROLES = {"org_owner", "org_admin", "analyst", "viewer"}
ADMIN_ROLES = {"platform_admin", "security_reviewer"}
PLATFORM_ROLES = ORG_ROLES | ADMIN_ROLES
ORG_MANAGEMENT_ROLES = {"org_owner", "org_admin"}
WORKSPACE_WRITE_ROLES = {"org_owner", "org_admin", "analyst"}

ROLE_PRIORITY = {
    "viewer": 10,
    "analyst": 20,
    "org_admin": 30,
    "org_owner": 40,
    "security_reviewer": 50,
    "platform_admin": 60,
}


def normalize_role(role: str) -> str:
    """Normalize a role string before permission checks."""
    return role.strip().lower()


def is_known_role(role: str) -> bool:
    """Return True when the role belongs to the scaffold RBAC set."""
    return normalize_role(role) in PLATFORM_ROLES


def has_any_role(role: str, allowed_roles: Iterable[str]) -> bool:
    """Return True when the current role is in the allowed set."""
    normalized_role = normalize_role(role)
    return normalized_role in {normalize_role(candidate) for candidate in allowed_roles}


def role_priority(role: str) -> int:
    """Return a comparable priority value for the current role."""
    return ROLE_PRIORITY.get(normalize_role(role), 0)


def choose_higher_role(*roles: str) -> str:
    """Return the highest-privilege role from the provided values."""
    known_roles = [normalize_role(role) for role in roles if role and is_known_role(role)]
    if not known_roles:
        return "analyst"
    return max(known_roles, key=role_priority)


def can_manage_workspace(role: str) -> bool:
    """Owners and admins can create/update workspace resources."""
    return has_any_role(role, ORG_MANAGEMENT_ROLES)


def can_manage_organization(role: str) -> bool:
    """Owners and admins can manage organization-scoped resources."""
    return has_any_role(role, ORG_MANAGEMENT_ROLES)


def can_write_workspace(role: str) -> bool:
    """Writers can submit work inside a visible workspace."""
    return has_any_role(role, WORKSPACE_WRITE_ROLES | ADMIN_ROLES)


def can_access_organization(
    role: str,
    principal_organization_id: str | None,
    target_organization_id: str,
) -> bool:
    """Allow access when the caller has platform scope or matches the target org."""
    normalized_target = target_organization_id.strip()
    return has_any_role(role, ADMIN_ROLES) or principal_organization_id == normalized_target


def can_access_workspace(
    role: str,
    principal_organization_id: str | None,
    target_organization_id: str,
    principal_workspace_id: str | None = None,
    target_workspace_id: str | None = None,
) -> bool:
    """Allow access when org scope matches or the caller has platform scope."""
    if has_any_role(role, ADMIN_ROLES):
        return True
    if principal_organization_id != target_organization_id:
        return False
    if can_manage_workspace(role):
        return True
    if target_workspace_id is None:
        return True
    return principal_workspace_id in {None, target_workspace_id}


def can_review_public_content(role: str) -> bool:
    """Platform admins and reviewers can operate the moderation queue."""
    return has_any_role(role, ADMIN_ROLES)
