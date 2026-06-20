def render_video(product, voice_file, output_file):
    try:
        import os

        # WICHTIG: safer ffmpeg render (forces valid mp4 writing)
        cmd = f"""
        ffmpeg -y \
        -f lavfi -i color=c=black:s=1080x1920:r=30:d=12 \
        -i {voice_file} \
        -c:v libx264 \
        -pix_fmt yuv420p \
        -c:a aac \
        -shortest \
        -movflags +faststart \
        {output_file}
        """

        os.system(cmd)

        # CHECK OB FILE WIRKLICH EXISTIERT
        if os.path.exists(output_file):
            return {
                "status": "VIDEO_RENDERED",
                "file": output_file
            }
        else:
            return {
                "status": "VIDEO_MISSING",
                "file": output_file
            }

    except Exception as e:
        return {
            "status": "VIDEO_ERROR",
            "error": str(e)
        }
