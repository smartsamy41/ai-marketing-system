from datetime import datetime, timezone


class NewsletterContentBuilder:


    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def build(
        self,
        campaign,
        product
    ):

        partner = campaign.get(
            "partner",
            ""
        )

        product_id = campaign.get(
            "product_id",
            ""
        )

        category = campaign.get(
            "category",
            ""
        )


        subject = (
            "Free Basics Empfehlung: "
            + category
        )


        html = f"""
<!DOCTYPE html>
<html>
<body>

<table width="100%" cellpadding="0" cellspacing="0">

<tr>
<td align="center">

<img src="https://freebasics.online/assets/brand/logo/free_basics_logo.png"
width="180"
alt="Free Basics">


<h1>
Free Basics
</h1>


<h2>
{category}
</h2>


<p>
Wir haben eine passende Information für dich zusammengestellt.
</p>


<p>
Produkt:
<strong>{product_id}</strong>
</p>


<p>
Partner:
{partner}
</p>


<p>
<strong>Werbung / Anzeige</strong>
</p>


<p>
Dieser Inhalt enthält externe Partnerangebote.
</p>


<a href="{product.get('landingpage_url','')}">
Vergleich starten
</a>


<hr>


<p>
Viele Grüße<br>
Free Basics
</p>


</td>
</tr>

</table>

</body>
</html>
"""


        return {

            "status": "CREATED",

            "subject":
                subject,

            "html":
                html,

            "created_at":
                self.now()

        }
