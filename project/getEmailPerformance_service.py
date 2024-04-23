from datetime import datetime
from typing import List

from pydantic import BaseModel


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


async def getEmailPerformance(emailId: str) -> EmailAnalyticsResponse:
    """
    Provides detailed analytics for a specific email. It fetches data such as the number of opens, clicks, and conversions directly related to the individual email ID. This detailed view helps in understanding the effectiveness of single email dispatches.

    Args:
        emailId (str): Unique identifier for the email whose analytics are being requested.

    Returns:
        EmailAnalyticsResponse: Aggregated data suitable for dashboards and reports showing email performance statistics.
    """
    import prisma.models

    metrics = await prisma.models.CampaignMetric.prisma().find_many(
        where={"EmailCampaign": {"id": emailId}}
    )
    opens_rates = [metric.openRate for metric in metrics]
    conversion_rates = [metric.conversionRate for metric in metrics]
    timestamps = [metric.createdAt for metric in metrics]
    total_emails_sent = len(metrics)
    average_open_rate = sum(opens_rates) / total_emails_sent
    average_conversion_rate = sum(conversion_rates) / total_emails_sent
    average_click_rate = average_open_rate * total_emails_sent / total_emails_sent
    trend_data = [
        EmailMetricTrends(
            date=metrics[i].createdAt, metric_value=opens_rates[i] + conversion_rates[i]
        )
        for i in range(total_emails_sent)
    ]
    return EmailAnalyticsResponse(
        total_emails_sent=total_emails_sent,
        average_open_rate=average_open_rate,
        average_click_through_rate=average_click_rate,
        average_conversion_rate=average_conversion_rate,
        trend_data=trend_data,
    )
