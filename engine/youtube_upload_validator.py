from pathlib import Path


class YouTubeUploadValidator:


    def validate(
        self,
        file_path,
        title,
        description,
        tags=None
    ):

        errors = []


        # Datei prüfen
        video = Path(file_path)

        if not video.exists():
            errors.append(
                "VIDEO_DATEI_FEHLT"
            )


        # Titel prüfen
        if not title:
            errors.append(
                "TITEL_FEHLT"
            )


        # Beschreibung prüfen
        if not description:
            errors.append(
                "BESCHREIBUNG_FEHLT"
            )


        # Werbung Hinweis
        if "Werbung" not in description:
            errors.append(
                "WERBUNG_HINWEIS_FEHLT"
            )


        # Free Basics Hinweis
        if "Free Basics" not in description:
            errors.append(
                "FREE_BASICS_FEHLT"
            )


        # Tags
        if not tags:
            errors.append(
                "TAGS_FEHLEN"
            )


        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
