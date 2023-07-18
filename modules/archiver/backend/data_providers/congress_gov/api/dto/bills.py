

from datetime import date, datetime
from typing import List, Literal
from pydantic import AnyHttpUrl, BaseModel


class BaseModelWithDetails(BaseModel):
    url: AnyHttpUrl

    # # The commented code is defining a computed field called `details` in the `BaseModelWithDetails`
    # @computed_field
    # @property
    # def details(self) -> List[BaseModel]:
    #     return CongressAPI().follow_link(self.url)


class ActionDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class CBOCostEstimateDTO(BaseModelWithDetails):
    description: str
    pubDate: datetime
    title: str
    url: AnyHttpUrl


class CommitteeReportDTO(BaseModelWithDetails):
    citation: str
    url: AnyHttpUrl


class CommitteesDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class AmendmentDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class LatestActionDTO(BaseModel):
    actionDate: date
    text: str


class LawDTO(BaseModel):
    number: str
    type: str


class PolicyAreaDTO(BaseModel):
    name: str


class RelatedBillsDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class SponsorDTO(BaseModel):
    bioguideId: str
    district: int
    firstName: str
    fullName: str
    isByRequest: str
    lastName: str
    middleName: str
    party: str
    state: str
    url: AnyHttpUrl


class SubjectsDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class SummariesDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class TextVersionsDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class TitlesDTO(BaseModelWithDetails):
    count: int
    url: AnyHttpUrl


class BillDetailsDTO(BaseModel):
    actions: ActionDTO  # summary
    amendments: AmendmentDTO  # summary
    cboCostEstimates: List[CBOCostEstimateDTO]
    committeeReports: List[CommitteeReportDTO]
    committees: CommitteesDTO
    congress: int
    constitutionalAuthorityStatementText: str
    cosponsors: SponsorDTO
    introducedDate: date
    latestAction: LatestActionDTO
    laws: List[LawDTO]
    number: str
    originChamber: str
    policyArea: PolicyAreaDTO
    relatedBills: RelatedBillsDTO
    sponsors: List[SponsorDTO]
    subjects: SubjectsDTO
    summaries: SummariesDTO
    textVersions: TextVersionsDTO
    title: str
    titles: TitlesDTO
    type: str
    updateDate: datetime
    updateDateIncludingText: datetime


class BillSummaryDTO(BaseModelWithDetails):
    congress: int
    latestAction: LatestActionDTO
    number: str
    originChamber: str
    originChamberCode: str
    title: str
    type: str
    updateDate: date
    updateDateIncludingText: datetime
    url: AnyHttpUrl


SUB_ENTITIES = Literal[
    "actions",
    "amendments",
    "committees",
    "cosponsors",
    "relatedbills",
    "subjects",
    "summaries",
    "text",
    "titles",
]