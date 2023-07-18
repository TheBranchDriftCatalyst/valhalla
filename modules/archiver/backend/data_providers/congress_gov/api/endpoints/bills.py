import json
from pydantic import AnyHttpUrl, BaseModel, computed_field
from datetime import date, datetime

from pydantic_core import Url
from backend.data_providers.congress_gov.api.congress_api import CongressAPI
from datetime import date, datetime
from typing import List, Literal, Optional, Union, get_args

from backend.data_providers.congress_gov.api.dto.bills import SUB_ENTITIES, BillDetailsDTO, BillSummaryDTO


class Bills(CongressAPI):
    RELATED_ENTITIES: List[Literal[SUB_ENTITIES]] = list(get_args(SUB_ENTITIES))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_recent_bills(self) -> List[BillSummaryDTO]:
        return self.get_bills()  # type: ignore - fix this idkw union is not really working

    def get_bills(
        self, congress=None, bill_type=None, bill_number=None, sub_entity=None
    ) -> Union[BillDetailsDTO, List[BillSummaryDTO], None]:
        url = self.build_url(congress, bill_type, bill_number, sub_entity)
        response = self.get(url)
        if bill_type and bill_number and congress and not sub_entity:
            return BillDetailsDTO.model_validate(response.get("bill", {}))
        elif not sub_entity:
            return list(map(BillSummaryDTO.model_validate, response.get("bills", [])))
        elif sub_entity in self.RELATED_ENTITIES:
            # TODO: gotta implement this at some point
            print('gotta deal with this at some point')
            # return SubEntityFactory(sub_entity).build(response.get(sub_entity, []))
            
        # we need to go to the entity's factory method to create the DTOs

    def build_url(
        self,
        congress: Optional[int] = None,
        bill_type: Optional[str] = None,
        bill_number: Optional[int] = None,
        sub_entity: Optional[SUB_ENTITIES]=None,
    ) -> str:
        endpoint = "bill"
        if congress:
            endpoint += f"/{congress}"
            if bill_type:
                endpoint += f"/{bill_type}"
                if bill_number:
                    endpoint += f"/{bill_number}"
                    if sub_entity and sub_entity in self.RELATED_ENTITIES:
                        endpoint += f"/{sub_entity}"
        return endpoint
