from dataclasses import dataclass
from datetime import datetime


@dataclass
class ColumnNames:
    description: str = 'description'
    item_id: str = 'item_id'
    order_date: str = 'order_date'
    last_updated: str = 'last_updated'
    status: str = 'status'


@dataclass
class EnrichedColumns:
    action_type: str = 'action_type'
    service_name: str = 'service_name'
    service_id: str = 'service_id'


class IDataRepository:
    def add_col(self, col_name: str, values: list):
        raise NotImplementedError

    def get_values_for(self, col_name: str) -> []:
        raise NotImplementedError