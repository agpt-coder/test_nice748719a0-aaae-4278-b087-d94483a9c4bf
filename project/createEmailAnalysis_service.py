from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CampaignDetail(BaseModel):
    """
    Detailed metrics concerning a specific campaign.
    """

    campaign_id: str
    open_rate: float
    conversion_rate: float


class EmailAnalysisResponse(BaseModel):
    """
    Provides detailed analytics of email campaigns over a given period. Includes key performance metrics like open rates and conversion rates, useful for strategic decision-making.
    """

    email_count: int
    average_open_rate: float
    average_conversion_rate: float
    detailed_metrics: List[CampaignDetail]


async def createEmailAnalysis(
    date_from: datetime, date_to: datetime, campaign_id: Optional[str] = None
) -> EmailAnalysisResponse:
    """
    Initiates a detailed analysis of newly sent emails within a given date range and possibly for a specific campaign.

    Args:
        date_from (datetime): Starting date for fetching emails for analytics.
        date_to (datetime): Ending date for fetching emails for analytics.
        campaign_id (Optional[str]): Optional campaign identifier to filter emails.

    Returns:
        EmailAnalysisResponse: Provides detailed analytics including open rates and conversion rates.
    """
    query_conditions = {
        "where": {"sentAt": {"gte": date_from, "lte": date_to}},
        "include": {"Metrics": True},
    }
    if campaign_id:
        query_conditions["where"].update({"id": campaign_id})
    campaigns = await prisma.models.EmailCampaign.prisma().find_many(**query_conditions)
    total_emails = 0
    total_open_rate = 0.0
    total_conversion_rate = 0.0
    campaign_details = []
    for campaign in campaigns:
        if campaign.Metrics:
            for metric in campaign.Metrics:
                total_emails += 1
                total_open_rate += metric.openRate
                total_conversion_rate += metric.conversionRate
                campaign_details.append(
                    CampaignDetail(
                        campaign_id=campaign.id,
                        open_rate=metric.openRate,
                        conversion_rate=metric.conversionRate,
                    )
                )
    if total_emails > 0:
        average_open_rate = total_open_rate / total_emails
        average_conversion_rate = total_conversion_rate / total_emails
    else:
        average_open_rate = 0.0
        average_conversion_rate = 0.0
    response = EmailAnalysisResponse(
        email_count=total_emails,
        average_open_rate=average_open_rate,
        average_conversion_rate=average_conversion_rate,
        detailed_metrics=campaign_details,
    )
    return response
