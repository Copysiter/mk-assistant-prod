from crud.base import CRUDBase  # noqa
from models import Role  # noqa
from schemas import RoleCreate, RoleUpdate  # noqa


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    pass


role = CRUDRole(Role)
