from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetEmailAnalyticsRequest(BaseModel):
    """
    This request model for retrieving email analytics doesn’t require user input fields but will ensure appropriate user roles.
    """

    pass


class EmailMetricTrends(BaseModel):
    """
    Structure representing trend over time for a particular metric.
    """

    date: datetime
    metric_value: float


class EmailAnalyticsResponse(BaseModel):
    """
    Aggregated data suitable for dashboards and reports showing email performance statistics.
    """

    total_emails_sent: int
    average_open_rate: float
    average_click_through_rate: float
    average_conversion_rate: float
    trend_data: List[EmailMetricTrends]


async def getAnalytics(request: GetEmailAnalyticsRequest) -> EmailAnalyticsResponse:
    """
    Retrieves overall performance statistics of sent emails. It pulls email outcome data from the
    AI Writing Module to provide key metrics and trends such as open rate, click-through rate,
    and conversion metrics. This endpoint serves aggregated data suitable for dashboards and reports.

    Args:
        request (GetEmailAnalyticsRequest): This request model for retrieving email analytics doesn’t require user input fields but will ensure appropriate user roles.

    Returns:
        EmailAnalyticsResponse: Aggregated data suitable for dashboards and reports showing email performance statistics.
    """
    campaign_metrics = await prisma.models.CampaignMetric.prisma().find_many()
    if not campaign_metrics:
        return EmailAnalyticsResponse(
            total_emails_sent=0,
            average_open_rate=0.0,
            average_click_through_rate=0.0,
            average_conversion_rate=0.0,
            trend_data=[],
        )
    total_open_rate = sum((metric.openRate for metric in campaign_metrics))
    total_conversion_rate = sum((metric.conversionRate for metric in campaign_metrics))
    total_emails_sent = len(campaign_metrics)
    average_open_rate = (
        total_open_rate / total_emails_sent if total_emails_sent > 0 else 0
    )
    average_conversion_rate = (
        total_conversion_rate / total_emails_sent if total_emails_sent > 0 else 0
    )
    average_click_through_rate = (average_open_rate + average_conversion_rate) / 2
    trend_data = sorted(
        [
            EmailMetricTrends(date=metric.createdAt, metric_value=metric.openRate)
            for metric in campaign_metrics
        ],
        key=lambda x: x.date,
    )
    response = EmailAnalyticsResponse(
        total_emails_sent=total_emails_sent,
        average_open_rate=average_open_rate,
        average_click_through_rate=average_click_through_rate,
        average_conversion_rate=average_conversion_rate,
        trend_data=trend_data,
    )
    return response
