from sqlalchemy.exc import SQLAlchemyError


class SortConfig:
    def __init__(self):
        pass

    def check_pass_true_property(self, sort_order: str,
                                 sort_by: str, model):
        if (sort_order != "asc" and sort_order != "desc"):
            raise SQLAlchemyError("Only 'asc' and 'desc' is allowed")
        if (not hasattr(model, sort_by) and sort_by != ''):
            raise SQLAlchemyError("Invalid Object Property")

    def get_config_query(self, sort_by: str, sort_order: str, model):
        self.check_pass_true_property(sort_order=sort_order, sort_by=sort_by, model=model)
        config_query = f"ORDER BY {sort_by} {sort_order}" if sort_by else ''
        return config_query
