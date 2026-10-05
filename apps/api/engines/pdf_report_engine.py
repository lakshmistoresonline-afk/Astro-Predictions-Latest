import html
import os

class PDFReportEngine:
    """
    PDFReportEngine compiles a publication-grade multi-page astrological treatise
    into a hardcopy-ready PDF or printable HTML document.
    Section 5 & 17 Compliance:
    - HTML-escapes all user-controlled text fields before inserting into HTML templates.
    - Reports ephemeris metadata accurately as NASA JPL DE440s.
    """

    @staticmethod
    def generate_html_treatise(report_data: dict) -> str:
        meta = report_data.get("metadata", {})
        native_raw = meta.get("native_name", "Native")
        title_raw = meta.get("report_title", "Masterwork Astrological Treatise")

        # Sanitize HTML user input
        native = html.escape(str(native_raw))
        report_title = html.escape(str(title_raw))
        engine_ver = html.escape(str(meta.get("engine_version", "Astrovision 2026.1 Canonical")))
        eph_provider = html.escape(str(meta.get("ephemeris", "NASA JPL DE440s")))

        c1_title = html.escape(str(report_data.get('chapter_1_methodology', {}).get('title', '')))
        c1_content = html.escape(str(report_data.get('chapter_1_methodology', {}).get('content', '')))
        c2_title = html.escape(str(report_data.get('chapter_2_ascendant', {}).get('title', '')))
        c2_content = html.escape(str(report_data.get('chapter_2_ascendant', {}).get('content', '')))

        doc_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{report_title}</title>
            <style>
                body {{ font-family: 'Times New Roman', serif; background: #ffffff; color: #111111; margin: 40px; line-height: 1.6; }}
                h1 {{ color: #b8860b; text-align: center; font-size: 28px; border-bottom: 2px solid #b8860b; padding-bottom: 10px; }}
                h2 {{ color: #b8860b; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 40px; }}
                .cover {{ text-align: center; page-break-after: always; padding-top: 150px; }}
                .cover h1 {{ font-size: 36px; border: none; }}
                .cover p {{ font-size: 18px; color: #555; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ccc; padding: 8px 12px; text-align: left; font-size: 14px; }}
                th {{ background: #f9f6ee; color: #b8860b; }}
                .chapter {{ page-break-inside: avoid; margin-bottom: 30px; }}
                .footer {{ text-align: center; font-size: 12px; color: #777; margin-top: 50px; border-top: 1px solid #eee; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="cover">
                <h1>{report_title}</h1>
                <p>Prepared exclusively for <b>{native}</b></p>
                <p>Generated via {engine_ver} | {eph_provider}</p>
                <p style="margin-top: 100px; font-style: italic;">"Astra inclinant, non obligant."</p>
            </div>

            <div class="chapter">
                <h2>Chapter 1: {c1_title}</h2>
                <p>{c1_content}</p>
            </div>

            <div class="chapter">
                <h2>Chapter 2: {c2_title}</h2>
                <p>{c2_content}</p>
            </div>
        """

        # Planetary table
        planets = report_data.get('chapter_3_planetary_positions', {}).get('data', {})
        if planets:
            doc_html += """
            <div class="chapter">
                <h2>Chapter 3: Planetary Positions & Dignities</h2>
                <table>
                    <tr><th>Planet</th><th>Sign</th><th>Degree</th><th>Nakshatra</th><th>Pada</th><th>Dignity</th></tr>
            """
            for p, d in planets.items():
                p_name = html.escape(str(p))
                p_sign = html.escape(str(d.get('sign', '')))
                p_deg = html.escape(str(d.get('degree', '')))
                p_nak = html.escape(str(d.get('nakshatra', '')))
                p_pada = html.escape(str(d.get('pada', '')))
                p_dig = html.escape(str(d.get('dignity', '')))
                doc_html += f"<tr><td><b>{p_name}</b></td><td>{p_sign}</td><td>{p_deg}°</td><td>{p_nak}</td><td>{p_pada}</td><td style='color:green;'>{p_dig}</td></tr>"
            doc_html += "</table></div>"

        # Life domains
        domains = report_data.get('chapter_9_life_domains', {}).get('data', [])
        if domains:
            doc_html += '<div class="chapter"><h2>Chapter 9: Master Life Domain Chapters</h2>'
            for dom in domains:
                dom_name = html.escape(str(dom.get('domain', '')))
                dom_focus = html.escape(str(dom.get('focus_areas', '')))
                dom_interp = html.escape(str(dom.get('traditional_interpretation', '')))
                doc_html += f"<h3>{dom_name}</h3><p><b>Focus:</b> {dom_focus}</p><p>{dom_interp}</p>"
            doc_html += '</div>'

        audit_disc = html.escape(str(report_data.get('chapter_12_audit_trail', {}).get('disclaimer', '')))
        audit_hash = html.escape(str(report_data.get('chapter_12_audit_trail', {}).get('calculation_hash', '')))

        doc_html += f"""
            <div class="footer">
                <p>{audit_disc}</p>
                <p>Calculation Hash: {audit_hash}</p>
            </div>
        </body>
        </html>"""
        return doc_html
