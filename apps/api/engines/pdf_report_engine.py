import os

class PDFReportEngine:
    """
    PDFReportEngine compiles a publication-grade multi-page astrological treatise
    into a hardcopy-ready PDF or printable HTML document.
    """

    @staticmethod
    def generate_html_treatise(report_data: dict) -> str:
        meta = report_data.get("metadata", {})
        native = meta.get("native_name", "Native")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{meta.get('report_title', 'Masterwork Astrological Treatise')}</title>
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
                <h1>{meta.get('report_title', 'Masterwork Astrological Treatise')}</h1>
                <p>Prepared exclusively for <b>{native}</b></p>
                <p>Generated via {meta.get('engine_version', 'Apex Engine')} | {meta.get('ephemeris', 'Swiss Ephemeris')}</p>
                <p style="margin-top: 100px; font-style: italic;">"Astra inclinant, non obligant."</p>
            </div>

            <div class="chapter">
                <h2>Chapter 1: {report_data.get('chapter_1_methodology', {}).get('title', '')}</h2>
                <p>{report_data.get('chapter_1_methodology', {}).get('content', '')}</p>
            </div>

            <div class="chapter">
                <h2>Chapter 2: {report_data.get('chapter_2_ascendant', {}).get('title', '')}</h2>
                <p>{report_data.get('chapter_2_ascendant', {}).get('content', '')}</p>
            </div>
        """

        # Planetary table
        planets = report_data.get('chapter_3_planetary_positions', {}).get('data', {})
        if planets:
            html += """
            <div class="chapter">
                <h2>Chapter 3: Planetary Positions & Dignities</h2>
                <table>
                    <tr><th>Planet</th><th>Sign</th><th>Degree</th><th>Nakshatra</th><th>Pada</th><th>Dignity</th></tr>
            """
            for p, d in planets.items():
                html += f"<tr><td><b>{p}</b></td><td>{d.get('sign')}</td><td>{d.get('degree')}°</td><td>{d.get('nakshatra')}</td><td>{d.get('pada')}</td><td style='color:green;'>{d.get('dignity')}</td></tr>"
            html += "</table></div>"

        # Life domains
        domains = report_data.get('chapter_9_life_domains', {}).get('data', [])
        if domains:
            html += '<div class="chapter"><h2>Chapter 9: Master Life Domain Chapters</h2>'
            for dom in domains:
                html += f"<h3>{dom.get('domain')}</h3><p><b>Focus:</b> {dom.get('focus_areas')}</p><p>{dom.get('traditional_interpretation')}</p>"
            html += '</div>'

        html += f"""
            <div class="footer">
                <p>{report_data.get('chapter_12_audit_trail', {}).get('disclaimer', '')}</p>
                <p>Calculation Hash: {report_data.get('chapter_12_audit_trail', {}).get('calculation_hash', '')}</p>
            </div>
        </body>
        </html>
        """
        return html
