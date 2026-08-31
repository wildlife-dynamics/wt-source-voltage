# Source Voltage Report — User Guide

This guide walks you through configuring and running the Source Voltage Report workflow (internal id `source_voltage`), which pulls GPS relocations and their embedded battery/collar-voltage telemetry from EarthRanger for a named subject group, compares the current period against a configurable previous period, and produces a per-subject historic voltage chart plus a merged Word doc report.

---

## Overview

For each subject in the selected group, the workflow delivers:

- A **historic voltage chart** — the subject's current-period voltage plotted against a min/mean/max band derived from the previous period (falls back to the current period's own band when no previous-period data is available)
- **2 combined GeoParquet exports** — all subjects' current-period and previous-period relocations, each with an extracted `voltage` column
- **A dashboard widget** — one merged "Collar Voltage" map/plot widget per subject group run
- **A Word doc report** (`overall_report.docx`) — cover page (with organisation logo, prepared-by, and report period) plus every subject's historic voltage chart, generated from a downloadable template

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with subject group observations whose `observation_details` include a battery/voltage field — the workflow looks for `battery`, `mainVoltage`, `batt`, or `power` (in that order) and uses whichever is present
- *(Optional)* An **organisation logo** file (PNG or JPG) to display on the Word report's cover page — only needed if you enable the Word doc report

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/wt-source-voltage.git
```

Then click **Add Template**.

---

### Step 2 — Configure an EarthRanger Connection

Navigate to **Data Sources** and click **Connect**, then select **EarthRanger**. Fill in the connection form:

- **Data Source Name** — a label to identify this connection
- **EarthRanger URL** — your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

---

### Step 3 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

---

### Step 4 — Set Workflow Details and Time Range

The configuration form opens with two sections at the top.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. subject group, site, or reporting period) |

**Time Range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the current analysis period |
| Until | End date and time of the current analysis period |

> Grouping is fixed to **Subject Name** — there is no grouping choice to make.

---

### Step 5 — Connect to EarthRanger and Set Subject Group

**Connect to EarthRanger**

Select the EarthRanger data source configured in Step 2 from the **Data Source** dropdown.

**Subject Group**

Enter the name of the EarthRanger subject group to analyse in the **Subject Group Name** field (default: `Elephants`). Each subject in the group is processed individually.

---

### Step 6 — Configure the Previous Period

**Previous Period**

Every option below computes a comparison period that ends on the same **Start Date** as your current time range (so the two periods never overlap) — only the comparison period's own Start Date changes:

| Mode | Description |
|------|-------------|
| Custom | Enter your own Years / Months / Weeks / Days offset (defaults to 1 month back) |
| Preset | Choose a common lookback: 1, 3, or 6 months, or 1 year back |
| Calendar | Pick an exact Start Date |

The previous period's relocations are used solely to compute the historic min/mean/max voltage band; if no previous-period data is found, the band collapses to the current period's own values.

---

### Step 7 — Configure the Word Doc Report

**Generate Word Doc Report**

| Field | Description |
|-------|-------------|
| Report Logo | Upload the organisation logo to display on the report cover page (PNG or JPG recommended). Required if you want a logo on the cover page; leave blank to omit it — the report still generates without one. |

Once all parameters are set, click **Submit**.

---

## Running the Workflow

Once submitted, the runner will:

1. Fetch subject group observations from EarthRanger for the current time range, convert `fixtime` to the analysis timezone, and derive relocations (dropping points at `(180,90)`, `(0,0)`, and `(1,1)`).
2. Fetch subject group observations for the computed previous period and process them the same way.
3. Sort both current and previous relocations by `fixtime` and persist each as GeoParquet (`relocations.parquet`, `previous_period_relocations.parquet`).
4. Extract a `voltage` column from each relocation set's `observation_details` JSON, checking the `battery`, `mainVoltage`, `batt`, and `power` fields in order.
5. Split both relocation sets by subject name and pair each subject's current and previous slices together.
6. Plot each subject's historic voltage chart — current-period voltage against the previous period's min/mean/max band (widened slightly if the band collapses to a single value; falls back to the current period alone when no previous-period data exists).
7. Build each chart's filename from a safe-string version of the subject's name (`<subject>_historic_voltage.html`), persist the chart HTML, and convert it to PNG.
8. Assemble a "Collar Voltage" map widget per subject and merge them into a single dashboard widget.
9. Download the Word report template and, if provided, the organisation logo.
10. Generate the merged Word doc report (`overall_report.docx`) — cover page (logo, prepared-by, report period) plus every subject's historic voltage chart.
11. Assemble the interactive dashboard (Collar Voltage Dashboard) and save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`. Files marked with `<subject>` are produced once per subject in the group.

### Per-subject outputs

| File | Description |
|------|-------------|
| `<subject>_historic_voltage.html` / `.png` | Historic voltage chart — current voltage vs. previous-period min/mean/max band |

### Combined outputs

| File | Description |
|------|-------------|
| `relocations.parquet` | All subjects' current-period relocations, including the extracted `voltage` column |
| `previous_period_relocations.parquet` | All subjects' previous-period relocations, including the extracted `voltage` column |
| `overall_report.docx` | Final Word doc report (cover page + every subject's historic voltage chart) |
