"""
Generate the Collar Voltage Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: collar_voltage_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "collar_voltage_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"Collar Voltage Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("Collar Voltage Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Per-subject historic collar/battery voltage monitoring", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>source_voltage</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>source_voltage</b> workflow fetches GPS relocations for a named "
      "EarthRanger subject group over a user-defined time range, extracts the "
      "collar/battery voltage embedded in each observation's details, and "
      "compares it against a matching previous period to build a historic "
      "voltage band per subject. Results are rendered as a chart, assembled "
      "into a dashboard widget, and merged into a Word doc report."),
    sp(4),
    p("For each subject the workflow delivers:"),
    bullet("A historic voltage chart — current-period voltage plotted against "
           "a min/mean/max band derived from the previous period (falls back "
           "to the current period's own values when no previous-period data "
           "is available)"),
    bullet("A PNG screenshot of that chart, used in the dashboard widget and "
           "the Word report"),
    bullet("A section in the merged Word doc report (<b>overall_report.docx</b>)"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Historic voltage charts", "1 per subject", "Current voltage vs. previous-period min/mean/max band"],
            ["GeoParquet exports",      "2 total",        "Current-period and previous-period relocations, each with a voltage column"],
            ["Dashboard widget",        "1 total",        "Merged 'Collar Voltage' map/plot widget across all subjects"],
            ["Word doc report",         "1 total",        "Cover page + one historic voltage chart per subject"],
        ],
        [4.5*cm, 3*cm, W - 7.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-platform",              ">=2.15.0, <2.16.0", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.1.0rc14.*",       "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.0rc1.*",        "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mep",     "1.0.1.*",           "ecoscope-workflows-custom"],
            ["pydeck",                         "0.9.2",             "conda-forge"],
            ["opentelemetry-sdk",              ">=1.20.0, <2.0.0",  "conda-forge"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connections"),
    make_table(
        [
            ["Connection", "Task", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch subject group observations for both the current and previous periods"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("2.3  Grouper"),
    p("The workflow groups all data by <b>name</b> (the renamed subject-name "
      "column). The <b>$defs</b> block in the spec restricts the grouper UI's "
      "<b>ValueGrouper.index_name</b> field to a single option, \"Subject "
      "Name\" — users cannot change the grouping dimension."),
    sp(6),
    h2("2.4  Subject group"),
    p("A user-provided string parameter (<b>Subject Group Name</b>, default: "
      "<i>Elephants</i>) is passed to both the current-period and "
      "previous-period observation fetches to scope the analysis to a single "
      "EarthRanger subject group. It is also threaded through unused for a "
      "future Word doc integration (comment: \"pass this to word doc\")."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. RELOCATION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Relocation Pipeline"),
    hr(),
    p("The current and previous periods run through an identical pipeline, "
      "in parallel, starting from their own <b>get_subjectgroup_observations</b> "
      "call."),
    sp(6),
    h2("3.1  Fetch and clean"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "get_subjectgroup_observations",
             "filter: clean, raise_on_empty: false, include_details: true, "
             "include_subjectsource_details: true"],
            ["2", "get_timezone_from_time_range → convert_values_to_timezone",
             "Convert the fixtime column to the analysis timezone (computed "
             "once from the current time range, reused for both periods)"],
            ["3", "process_relocations",
             "Retain 12 columns: groupby_col, fixtime, junk_status, geometry, "
             "extra__subject__name, extra__subject__hex, extra__subject__sex, "
             "extra__created_at, extra__subject__subject_subtype, "
             "extra__subjectsource__id, extra__subjectsource__assigned_range, "
             "extra__observation_details. Filter 3 invalid coordinate pairs: "
             "(180,90), (0,0), (1,1)"],
            ["4", "sort_values",
             "Sort by fixtime, ascending, nulls last"],
            ["5", "persist_df",
             "Persist as GeoParquet to $ECOSCOPE_WORKFLOWS_RESULTS "
             "(relocations.parquet / previous_period_relocations.parquet)"],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.2  Previous Period selection"),
    p("The comparison period is computed by "
      "<b>ecoscope_workflows_ext_ste.tasks.filter.flexible_previous_period</b>, "
      "exposed to the user as a \"Previous Period\" task-group. It always ends "
      "on the current time range's Start Date, so the two periods never "
      "overlap:"),
    make_table(
        [
            ["Mode", "Description"],
            ["Custom",   "User-supplied Years / Months / Weeks / Days offset (default: 1 month back)"],
            ["Preset",   "A common lookback: 1, 3, or 6 months, or 1 year back"],
            ["Calendar", "An exact Start Date"],
        ],
        [3*cm, W - 3*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. VOLTAGE EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Voltage Extraction"),
    hr(),
    p("Both relocation sets go through <b>extract_value_from_json_column</b> "
      "against their <b>observation_details</b> column, producing a float "
      "<b>voltage</b> column:"),
    make_table(
        [
            ["Parameter", "Value"],
            ["column_name",        "observation_details"],
            ["field_name_options", "battery, mainVoltage, batt, power (checked in this order)"],
            ["output_type",        "float"],
            ["output_column_name", "voltage"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(4),
    note("This generalized field-name lookup replaces an earlier, "
         "collar-model-specific voltage extraction task, so the workflow "
         "tolerates different EarthRanger device integrations reporting "
         "battery/voltage under different JSON keys."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. HISTORIC VOLTAGE CHART
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Historic Voltage Chart"),
    hr(),
    h2("5.1  Per-subject fan-out"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "split_groups",
             "Split current and previous relocations by the configured grouper (name)"],
            ["2", "column_first_unique_value",
             "Get each subject's display name from the current-period slice"],
            ["3", "safe_string (ext_ste)",
             "Sanitize the subject name for use in a filename"],
            ["4", "prefix_string_var",
             "Build the chart filename: <safe_subject_name>_historic_voltage.html"],
            ["5", "groupbykey",
             "Pair each subject's current-period slice with its previous-period "
             "slice (zip_current_prev_name)"],
        ],
        [1.2*cm, 3.5*cm, W - 4.7*cm],
    ),
    sp(6),
    h2("5.2  Plotting"),
    p("<b>plot_historic_voltage</b> (column: voltage) draws the subject's "
      "current voltage series against a band built from the previous "
      "period's 2.5th/97.5th percentile and mean. If the previous-period "
      "slice is missing or empty, the current period's own values are used "
      "for the band instead, so a chart still renders on a subject's first "
      "run. If the computed band collapses to a single value, it is widened "
      "by ±2.5% so the shaded region remains visible."),
    sp(6),
    h2("5.3  Persisting and rendering"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "groupbykey",
             "Pair each chart's filename with its rendered HTML "
             "(historic_voltage_text); skipped if any dependency was skipped "
             "or any keyed pair is a skip"],
            ["2", "persist_text",
             "Write the chart HTML to $ECOSCOPE_WORKFLOWS_RESULTS "
             "(filename_suffix: none — the filename built in step 5.1 is used verbatim)"],
            ["3", "create_map_widget_single_view",
             "Title: \"Collar Voltage\"; skipif: never, so a widget is always "
             "created even if the underlying chart data is empty"],
            ["4", "merge_widget_views",
             "Merge every subject's widget into a single dashboard widget"],
            ["5", "html_to_png",
             "device_scale_factor: 2.0, wait_for_timeout: 10 ms, "
             "max_concurrent_pages: 1, full_page: false"],
        ],
        [1.2*cm, 3.5*cm, W - 4.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. WORD DOC REPORT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Word Doc Report"),
    hr(),
    p("The report template (<b>source_voltage_report.docx</b>) is downloaded "
      "once via <b>fetch_and_persist_file</b> (ecoscope_workflows_ext_ste) "
      "from a fixed Dropbox URL, with up to 3 retries and "
      "overwrite_existing: false."),
    sp(6),
    h2("6.1  Report Logo"),
    p("The \"Generate Word Doc Report\" task-group exposes a single field, "
      "<b>Report Logo</b>, backed by <b>get_file_path</b>. It accepts an "
      "uploaded PNG/JPG saved under $ECOSCOPE_WORKFLOWS_RESULTS. This field "
      "is optional — the report still generates without a logo."),
    sp(6),
    h2("6.2  Generation"),
    p("<b>generate_source_voltage_report</b> (ecoscope_workflows_ext_mep) "
      "walks $ECOSCOPE_WORKFLOWS_RESULTS for image files, classifies "
      "<i>_historic_voltage</i>-suffixed images by subject (stripping the "
      "suffix) and any other image by its full filename stem, renders them "
      "all into the template's voltage-chart list, and adds the cover-page "
      "fields below:"),
    make_table(
        [
            ["Field", "Value"],
            ["org_logo_path",  "The uploaded Report Logo, or none (cover page omits it)"],
            ["report_period",  "The current time range (Since — Until)"],
            ["prepared_by",    '"Ecoscope"'],
            ["filename",       "overall_report.docx"],
        ],
        [5*cm, W - 5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Dashboard"),
    hr(),
    p("<b>gather_dashboard</b> assembles the final interactive dashboard from "
      "the workflow details, the current time range, the configured grouper, "
      "and the single merged Collar Voltage widget produced in Section 5.3."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Output Files"),
    hr(),
    p("All outputs are written to <b>$ECOSCOPE_WORKFLOWS_RESULTS</b>. Files "
      "marked with <i>&lt;subject&gt;</i> are produced once per subject in "
      "the group."),
    make_table(
        [
            ["File", "Description"],
            ["<subject>_historic_voltage.html / .png",
             "Historic voltage chart — current voltage vs. previous-period min/mean/max band"],
            ["relocations.parquet",
             "All subjects' current-period relocations, including the extracted voltage column"],
            ["previous_period_relocations.parquet",
             "All subjects' previous-period relocations, including the extracted voltage column"],
            ["source_voltage_report.docx",
             "Downloaded report template (intermediate asset, not a final deliverable)"],
            ["overall_report.docx",
             "Final Word doc report (cover page + every subject's historic voltage chart)"],
        ],
        [7*cm, W - 7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Workflow Execution Logic"),
    hr(),
    h2("9.1  Global skip conditions"),
    p("The top-level <b>task-instance-defaults</b> block applies two skip "
      "conditions to every task unless overridden:"),
    bullet("<b>any_is_empty_df</b> — skips the task if any upstream "
           "DataFrame dependency is empty"),
    bullet("<b>any_dependency_skipped</b> — skips the task if any upstream "
           "task was skipped"),
    p("Two tasks override this default:"),
    bullet("<b>collared_voltage_widget</b> uses <b>skipif: conditions: "
           "[never]</b>, so a dashboard widget is always created even if the "
           "underlying chart data is empty"),
    bullet("<b>historic_voltage_text</b> uses <b>any_dependency_skipped</b> "
           "plus <b>any_keyed_iterables_are_skips</b> (unpack_depth: 1), so "
           "an individual subject's filename/chart pair is skipped without "
           "failing the whole zip"),
    sp(6),
    h2("9.2  mapvalues fan-out"),
    p("Per-subject processing runs in parallel via <b>mapvalues</b>. The "
      "fan-out starts at <b>split_groups</b> (current and previous relocations, "
      "independently) and continues through:"),
    bullet("split_current_relocs / split_previous_relocs → "
           "column_first_unique_value → safe_string → prefix_string_var "
           "(build each subject's chart filename)"),
    bullet("groupbykey (zip_current_prev_name) → plot_historic_voltage → "
           "groupbykey (historic_voltage_text) → persist_text → "
           "create_map_widget_single_view → html_to_png"),
    sp(6),
    h2("9.3  Screenshot timing"),
    p("The historic voltage chart screenshot uses: wait_for_timeout: 10 ms, "
      "device_scale_factor: 2.0, max_concurrent_pages: 1, full_page: false — "
      "the same configuration used across other Ecoscope chart-to-PNG steps."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned"],
            ["ecoscope-platform",              ">=2.15.0, <2.16.0"],
            ["ecoscope-workflows-ext-custom",  "0.1.0rc14.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.0rc1.*"],
            ["ecoscope-workflows-ext-mep",     "1.0.1.*"],
            ["pydeck",                         "0.9.2"],
            ["opentelemetry-sdk",              ">=1.20.0, <2.0.0"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    note("All packages are resolved from the prefix.dev Ecoscope conda "
         "channels. The wildcard patch-version pin (.*) allows bug-fix "
         "releases to be picked up automatically while keeping minor and "
         "major versions locked. ecoscope-workflows-ext-ste is pinned to a "
         "pre-release (0.0.0rc1.*)."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
