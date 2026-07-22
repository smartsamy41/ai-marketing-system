from pathlib import Path


class ASSSubtitleRenderer:


    def create(
        self,
        subtitles,
        filename="subtitle.ass"
    ):

        folder = Path(
            "generated_videos/subtitles"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        path = folder / filename


        header = """
[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Alignment, MarginV

Style: Default,Arial,32,&H00FFFFFF,&H00000000,&H80000000,2,180

[Events]
Format: Start, End, Style, Text
"""


        def timestamp(seconds):

            h = int(seconds // 3600)
            m = int((seconds % 3600)//60)
            s = seconds % 60

            return f"{h}:{m:02}:{s:05.2f}"


        with open(path,"w") as f:

            f.write(header)

            for item in subtitles:

                text = item["text"].replace("\n"," ")

                f.write(
                    "Dialogue: "
                    f"{timestamp(item['start'])},"
                    f"{timestamp(item['end'])},"
                    "Default,"
                    f"{text}\n"
                )


        return str(path)
