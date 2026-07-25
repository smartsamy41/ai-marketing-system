from engine.newsletter_decision_engine import NewsletterDecisionEngine


class AICampaignNewsletterBridge:

    def __init__(self):
        self.decision = NewsletterDecisionEngine()

    def evaluate(self, campaign):

        partner = campaign.get("partner", "")

        result = self.decision.check(partner)

        return {
            "campaign_id": campaign.get("campaign_id"),
            "partner": partner,
            "decision": result.get("decision"),
            "reason": result.get("reason", ""),
            "mode": result.get("mode", "")
        }
