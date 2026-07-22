from html import escape


def get_cookie_consent_script() -> str:
    """
    Zeigt einen Hinweis für technisch notwendige Speicherung an.

    Aktuell werden über diesen Baustein keine optionalen Analyse-,
    Marketing- oder Drittanbieter-Cookies aktiviert.
    """
    return """
    <div
      id="cookie-banner"
      role="dialog"
      aria-live="polite"
      aria-label="Datenschutz und technisch notwendige Speicherung"
      style="
        position:fixed;
        right:1rem;
        bottom:1rem;
        left:1rem;
        z-index:9999;
        display:none;
        max-width:900px;
        margin:0 auto;
        padding:1rem;
        color:#ffffff;
        background:#0f172a;
        border:1px solid #334155;
        border-radius:10px;
        box-shadow:0 12px 30px rgba(15,23,42,0.35);
      "
    >
      <div
        style="
          display:flex;
          align-items:center;
          justify-content:space-between;
          gap:1rem;
          flex-wrap:wrap;
        "
      >
        <div style="flex:1; min-width:260px; font-size:0.9rem; line-height:1.55;">
          <strong>Datenschutz und Transparenz</strong>
          <br>
          Diese Website verwendet derzeit nur technisch notwendige Funktionen
          für den sicheren Betrieb. Weitere Informationen findest du in unserer
          <a
            href="/datenschutz"
            style="color:#93c5fd; text-decoration:underline;"
          >Datenschutzerklärung</a>.
        </div>

        <button
          id="cookie-essential-button"
          type="button"
          style="
            padding:0.65rem 1rem;
            color:#ffffff;
            background:#2563eb;
            border:0;
            border-radius:6px;
            cursor:pointer;
            font-weight:700;
          "
        >
          Verstanden
        </button>
      </div>
    </div>

    <script>
      (function () {
        "use strict";

        const storageKey = "freebasics_cookie_notice";
        const banner = document.getElementById("cookie-banner");
        const button = document.getElementById("cookie-essential-button");

        if (!banner || !button) {
          return;
        }

        try {
          if (!localStorage.getItem(storageKey)) {
            banner.style.display = "block";
          }
        } catch (error) {
          banner.style.display = "block";
        }

        button.addEventListener("click", function () {
          try {
            localStorage.setItem(storageKey, "acknowledged");
          } catch (error) {
            console.warn("Cookie-Hinweis konnte nicht gespeichert werden.");
          }

          banner.style.display = "none";
        });
      }());
    </script>
    """


def get_eeat_footer() -> str:
    """
    Gemeinsamer Footer für Transparenz-, Redaktions- und Rechtsseiten.
    """
    return """
    <footer
      style="
        margin-top:4rem;
        padding:3rem 1.5rem 1.5rem;
        color:#cbd5e1;
        background:#0f172a;
        border-top:1px solid #334155;
      "
    >
      <div
        style="
          display:grid;
          grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
          gap:2rem;
          max-width:1200px;
          margin:0 auto;
        "
      >
        <section aria-labelledby="footer-free-basics">
          <h2
            id="footer-free-basics"
            style="margin:0 0 1rem; color:#ffffff; font-size:1rem;"
          >
            Free Basics
          </h2>

          <p style="margin:0; font-size:0.88rem; line-height:1.6;">
            Wissensplattform für Tarifinformationen, digitale Themen und
            Verbraucherorientierung. Affiliate-Bereiche werden transparent
            als Werbung oder Anzeige gekennzeichnet.
          </p>
        </section>

        <nav aria-labelledby="footer-transparenz">
          <h2
            id="footer-transparenz"
            style="margin:0 0 1rem; color:#ffffff; font-size:1rem;"
          >
            Redaktion und Transparenz
          </h2>

          <ul
            style="
              margin:0;
              padding:0;
              list-style:none;
              font-size:0.88rem;
              line-height:1.9;
            "
          >
            <li>
              <a href="/methodik" style="color:#cbd5e1;">
                Methodik
              </a>
            </li>
            <li>
              <a href="/redaktion" style="color:#cbd5e1;">
                Redaktionelle Richtlinien
              </a>
            </li>
            <li>
              <a href="/affiliate-hinweis" style="color:#cbd5e1;">
                Affiliate-Hinweis
              </a>
            </li>
          </ul>
        </nav>

        <nav aria-labelledby="footer-rechtliches">
          <h2
            id="footer-rechtliches"
            style="margin:0 0 1rem; color:#ffffff; font-size:1rem;"
          >
            Rechtliches
          </h2>

          <ul
            style="
              margin:0;
              padding:0;
              list-style:none;
              font-size:0.88rem;
              line-height:1.9;
            "
          >
            <li>
              <a href="/impressum" style="color:#cbd5e1;">
                Impressum
              </a>
            </li>
            <li>
              <a href="/datenschutz" style="color:#cbd5e1;">
                Datenschutzerklärung
              </a>
            </li>
            <li>
              <a href="/agb" style="color:#cbd5e1;">
                AGB
              </a>
            </li>
          </ul>
        </nav>
      </div>

      <div
        style="
          max-width:1200px;
          margin:2rem auto 0;
          padding-top:1.5rem;
          border-top:1px solid #334155;
          text-align:center;
          font-size:0.8rem;
        "
      >
        &copy; 2026 Free Basics. Alle Rechte vorbehalten.
      </div>
    </footer>
    """
