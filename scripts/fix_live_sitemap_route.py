from pathlib import Path


file = Path("app/main.py")

text = file.read_text(
    encoding="utf-8"
)


start = text.index(
    '@app.get(\n    "/sitemap.xml"'
)


end = text.index(
    '@app.get(\n    "/social-card.png"',
    start
)


new_block = r'''
@app.get(
    "/sitemap.xml",
    response_class=Response
)
def sitemap_xml():

    sitemap_file = Path(
        "public_web_assets/sitemap.xml"
    )

    if not sitemap_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Production sitemap not found"
        )


    xml = sitemap_file.read_text(
        encoding="utf-8"
    )


    return Response(
        content=xml,
        media_type="application/xml; charset=utf-8"
    )


'''


new_text = (
    text[:start]
    +
    new_block
    +
    text[end:]
)


file.write_text(
    new_text,
    encoding="utf-8"
)


print("SITEMAP ROUTE FIXED")
