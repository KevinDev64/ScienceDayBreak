# Готовые зависимости для каждой роли
from database import Role
from helpers import RoleChecker

require_admin = RoleChecker([Role.ADMIN])
require_operator = RoleChecker([Role.ADMIN, Role.OPERATOR])
require_user = RoleChecker([Role.ADMIN, Role.OPERATOR, Role.USER])

# Только конкретная роль (без иерархии)
require_only_admin = RoleChecker([Role.ADMIN])
require_only_operator = RoleChecker([Role.OPERATOR])
require_only_user = RoleChecker([Role.USER])
