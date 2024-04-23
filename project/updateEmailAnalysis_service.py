from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class EmailAnalyticsUpdatedResponse(BaseModel):
    """
    Provides the newly updated metrics for an email campaign to reflect any corrections made through the patch request.
    """

    emailId: str
    openRate: float
    conversionRate: float
    updateStatus: str


async def updateEmailAnalysis(
    emailId: str, openRate: Optional[float], conversionRate: Optional[float]
) -> EmailAnalyticsUpdatedResponse:
    """
    Updates existing analytics data for a specific email. This endpoint accommodates changes or recalculations in email performance metrics and can be used to correct or enhance analytics accuracy.

    Args:
        emailId (str): The unique identifier for the email campaign for which metrics are being updated.
        openRate (Optional[float]): The updated open rate for the email campaign. This is optional.
        conversionRate (Optional[float]): The updated conversion rate for the email campaign. This is optional.

    Returns:
        EmailAnalyticsUpdatedResponse: Provides the newly updated metrics for an email campaign to reflect any corrections made through the patch request.
    """
    metrics = await prisma.models.CampaignMetric.prisma().find_many(
        where={"emailCampaignId": emailId}
    )
    if not metrics:
        return EmailAnalyticsUpdatedResponse(
            emailId=emailId,
            openRate=None,
            conversionRate=None,
            updateStatus="Failed: Email campaign not found",
        )
    current_metric = metrics[0]
    updated_data = {}
    if openRate is not None:
        updated_data["openRate"] = openRate
    if conversionRate is not None:
        updated_data["conversionRate"] = conversionRate
    if updated_data:
        updated_metric = await prisma.models.CampaignMetric.prisma().update(
            where={"id": current_metric.id}, data=updated_data
        )
        updateStatus = "Success: Metrics updated"
    else:
        updated_metric = current_metric
        updateStatus = "No change: No updates provided"
    return EmailAnalyticsUpdatedResponse(
        emailId=emailId,
        openRate=getattr(updated_metric, "openRate", None),
        conversionRate=getattr(updated_metric, "conversionRate", None),
        updateStatus=updateStatus,
    )
