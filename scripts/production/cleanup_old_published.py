from pathlib import Path
import shutil


landingpages = [
    "maybelline-new-york-sky-high-mascara-fuer-extreme-laenge-und-volumen-very-black-7,2-ml.html",
    "philips-oneblade-360-face-&-body-elektrischer-rasierer-trimmer-und-bodygroomer-qp2824",
    "philips-oneblade-intimate-intimrasur-trimmen-und-rasieren-mit-extra-hautschutz-modell-qp1924",
    "philips-oneblade-original-360-klingen-passend-fuer-alle-oneblade-und-pro-modelle-4er-pack-qp440",
    "tv-+-internet-+-festnetz.html"
]


articles = [
    "das-cafe-am-rande-der-welt-eine-erzaehlung-ueber-den-sinn-des-lebens-ratgeber.html",
    "das-café-am-rande-der-welt-eine-erzaehlung-ueber-den-sinn-des-lebens-ratgeber.html",
    "lego editions kylian mbappé fussball-highlights spielzeug 3d modellbau mit minifigur-ratgeber.html",
    "lego-editions-kylian-mbappe-fussball-highlights-spielzeug-3d-modellbau-mit-minifigur-ratgeber.html",
    "lego-editions-kylian-mbappé-fussball-highlights-spielzeug-3d-modellbau-mit-minifigur-ratgeber.html",
    "maybelline-new-york-sky-high-mascara-fuer-extreme-laenge-und-volumen-very-black-7,2-ml-ratgeber.html",
    "philips-oneblade-360-face-&-body-elektrischer-rasierer-trimmer-und-bodygroomer-qp2824",
    "philips-oneblade-intimate-intimrasur-trimmen-und-rasieren-mit-extra-hautschutz-modell-qp1924",
    "philips-oneblade-original-360-klingen-passend-fuer-alle-oneblade-und-pro-modelle-4er-pack-qp440",
    "tv-+-internet-+-festnetz-ratgeber.html"
]


def remove_path(path):

    if path.exists():

        if path.is_dir():

            shutil.rmtree(path)

            print(
                "DELETED DIRECTORY:",
                path.name
            )

        else:

            path.unlink()

            print(
                "DELETED FILE:",
                path.name
            )


lp_dir = Path(
    "content_repository/landingpages/published"
)


article_dir = Path(
    "content_repository/articles/published"
)


for name in landingpages:

    remove_path(
        lp_dir / name
    )



for name in articles:

    remove_path(
        article_dir / name
    )


print()
print("CLEANUP COMPLETE")
