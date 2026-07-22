from googleapiclient.http import MediaFileUpload


class YouTubeUploader:


    def __init__(self, youtube_client):

        self.youtube = youtube_client


    def upload(
        self,
        file_path: str,
        title: str,
        description: str,
        tags=None
    ):


        if tags is None:
            tags = []


        request = self.youtube.videos().insert(

            part="snippet,status",

            body={

                "snippet": {

                    "title": title,

                    "description": description,

                    "tags": tags,

                    "categoryId": "22",

                    "defaultLanguage": "de"

                },


                "status": {

                    "privacyStatus": "private",

                    "selfDeclaredMadeForKids": False

                }

            },


            media_body=MediaFileUpload(
                file_path,
                mimetype="video/mp4"
            )

        )


        return request.execute()
