from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class QualityCheckSummary(BaseModel):
    """
    Describes a brief summary of a quality check for a piece of content.
    """

    validation_id: str
    submission_time: datetime
    status: str


class ListQualityChecksResponse(BaseModel):
    """
    Provides a list of quality checks along with relevant data such as ID, submission time, and current status.
    """

    validations: List[QualityCheckSummary]


async def listValidations(
    limit: Optional[int] = None, offset: Optional[int] = None
) -> ListQualityChecksResponse:
    """
    Lists recent content validations submitted to the module. Provides a summary of each validation, including IDs, submission times, and status.

    Args:
        limit (Optional[int]): Limits the number of validation summaries returned.
        offset (Optional[int]): Skips the specified number of records before beginning to return the summaries.

    Returns:
        ListQualityChecksResponse: Provides a list of quality checks along with relevant data such as ID, submission time, and current status.
    """
    drafts = await prisma.models.Draft.prisma().find_many(
        take=limit, skip=offset, where={"status": "EDITED"}, order={"createdAt": "desc"}
    )
    summaries = [
        QualityCheckSummary(
            validation_id=draft.id, submission_time=draft.createdAt, status=draft.status
        )
        for draft in drafts
    ]
    return ListQualityChecksResponse(validations=summaries)
