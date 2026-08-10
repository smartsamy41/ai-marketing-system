from datetime import datetime, timezone, timedelta
import json
from pathlib import Path


class EventResolver:

    def __init__(self):

        self.file = Path(
            "data_master/event_layer/event_registry.json"
        )

        self.events = self.load()


    def load(self):

        if not self.file.exists():
            return []

        with open(
            self.file,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data.get(
            "events",
            []
        )


    def active_events(self):

        today = datetime.now(
            timezone.utc
        ).date()

        result = []

        for event in self.events:

            start = datetime.strptime(
                event["start_date"],
                "%Y-%m-%d"
            ).date()

            end = datetime.strptime(
                event["end_date"],
                "%Y-%m-%d"
            ).date()

            if start <= today <= end:

                result.append(event)

        return result


    def preparation_events(self):

        today = datetime.now(
            timezone.utc
        ).date()

        result = []

        for event in self.events:

            start = datetime.strptime(
                event["start_date"],
                "%Y-%m-%d"
            ).date()

            prepare_days = int(
                event.get(
                    "prepare_days_before",
                    14
                )
            )

            preparation_start = (
                start -
                timedelta(
                    days=prepare_days
                )
            )


            if preparation_start <= today <= start:

                result.append(event)

        return result


    def upcoming_events(self):

        today = datetime.now(
            timezone.utc
        ).date()

        result = []

        for event in self.events:

            start = datetime.strptime(
                event["start_date"],
                "%Y-%m-%d"
            ).date()


            if start >= today:

                result.append(event)


        return sorted(
            result,
            key=lambda x: x["start_date"]
        )
