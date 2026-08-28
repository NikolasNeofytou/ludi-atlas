#!/usr/bin/env python3
"""Generate the Ludi venue-atlas pipeline brief as LaTeX from venues.json."""
import json
import sys
from datetime import date
from pathlib import Path

VENUES = Path.home() / "Desktop/ludi-atlas/venues.json"
OUT = Path(__file__).parent / "report.tex"

STAGES = [
    ("unqualified", "Unqualified", "5F6E73"),
    ("contacted", "Contacted", "D99520"),
    ("visited", "Visited", "8A5A0E"),
    ("proposal", "Proposal", "175E77"),
    ("onboarding", "Onboarding", "35836B"),
    ("live", "Live", "1F6640"),
    ("lost", "Lost", "7E4A4A"),
]
STAGE_LABEL = {k: l for k, l, _ in STAGES}
STAGE_ORDER = ["live", "onboarding", "proposal", "visited", "contacted", "unqualified", "lost"]
DISTRICTS = ["Limassol", "Larnaca", "Nicosia", "Paphos", "Famagusta"]
DONE = {"live", "lost"}

CHARMAP = {
    "★": r"$\star$", "→": r"$\rightarrow$", "—": "---", "–": "--",
    "€": r"\euro{}", "×": r"$\times$", "≈": r"$\approx$",
}


def esc(s):
    s = str(s or "")
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        s = s.replace(a, b)
    for a, b in CHARMAP.items():
        s = s.replace(a, b)
    return s


def overdue(v, today):
    return bool(v["next_date"]) and v["next_date"] < today and v["stage"] not in DONE


def venue_entry(v, today):
    od = overdue(v, today)
    bits = " · ".join(esc(x) for x in [v["area"], v["phone"], v["pitches"]] if x)
    out = [r"\begin{venue}"]
    out.append(rf"\venuename{{{esc(v['name'])}}}{{{esc(v['owner'])}}}{{s{v['stage']}}}")
    out.append(rf"\venuemeta{{{STAGE_LABEL[v['stage']]} · {bits}}}")
    if v["flags"]:
        out.append(rf"\venueflags{{{esc(' · '.join(v['flags']))}}}")
    if v["next_action"]:
        due = f" (by {esc(v['next_date'])}{' --- overdue' if od else ''})" if v["next_date"] else ""
        cmd = "venueactod" if od else "venueact"
        out.append(rf"\{cmd}{{{esc(v['next_action'])}{due}}}")
    for e in reversed(v["log"][-2:]):
        out.append(rf"\venuelog{{{esc(e['date'])}}}{{{esc(e['text'])}}}")
    out.append(r"\end{venue}")
    return "\n".join(out)


def main():
    today = date.today().isoformat()
    venues = json.loads(VENUES.read_text())
    for v in venues:
        for k in ["area", "phone", "pitches", "next_action", "next_date", "owner", "stage"]:
            v.setdefault(k, "")
        v.setdefault("flags", [])
        v.setdefault("log", [])
        v.setdefault("district", "Limassol")

    counts = {}
    for v in venues:
        counts[v["stage"]] = counts.get(v["stage"], 0) + 1
    n_live = counts.get("live", 0)
    n_od = sum(1 for v in venues if overdue(v, today))

    chips = quad_join = r"\hspace{14pt}"
    chips = quad_join.join(
        rf"\chip{{s{k}}}{{{l}}}{{{counts.get(k, 0)}}}" for k, l, _ in STAGES
    )

    nxt = [v for v in venues if v["stage"] not in DONE and (v["next_action"] or v["next_date"])]
    nxt.sort(key=lambda v: (not overdue(v, today), v["next_date"] or "9999", v["name"]))
    next_rows = "\n".join(
        (r"\rowod" if overdue(v, today) else r"\row")
        + f"{{{esc(v['next_date'] or '---')}}}{{{esc(v['name'])}}}{{{esc(v['owner'])}}}{{{esc(v['next_action'] or '---')}}}"
        for v in nxt
    )

    sections = []
    for d in DISTRICTS:
        dv = [v for v in venues if v["district"] == d]
        if not dv:
            continue
        sections.append(rf"\district{{{d}}}{{{len(dv)}}}")
        for stage in STAGE_ORDER:
            sv = sorted((v for v in dv if v["stage"] == stage), key=lambda v: v["name"])
            if not sv:
                continue
            sections.append(rf"\stagehead{{s{stage}}}{{{STAGE_LABEL[stage]}}}{{{len(sv)}}}")
            sections.extend(venue_entry(v, today) for v in sv)
    body = "\n".join(sections)

    colordefs = "\n".join(rf"\definecolor{{s{k}}}{{HTML}}{{{h}}}" for k, _, h in STAGES)

    tex = TEMPLATE
    for key, val in [
        ("@COLORDEFS@", colordefs), ("@DATE@", today), ("@CHIPS@", chips),
        ("@NVEN@", str(len(venues))), ("@NLIVE@", str(n_live)), ("@NOD@", str(n_od)),
        ("@NEXTROWS@", next_rows), ("@BODY@", body),
    ]:
        tex = tex.replace(key, val)
    OUT.write_text(tex)
    print(f"wrote {OUT} ({len(venues)} venues, {len(nxt)} next steps)")


TEMPLATE = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[margin=16mm,top=14mm,bottom=16mm]{geometry}
\usepackage{fontspec,xcolor,longtable,array,graphicx,eurosym,amssymb}
\usepackage[hidelinks]{hyperref}
\setmainfont{Helvetica Neue}
\newfontfamily\display{Georgia}
\setmonofont{Menlo}[Scale=0.82]
\definecolor{chalk}{HTML}{10181C}
\definecolor{chalkdim}{HTML}{3F4C51}
\definecolor{chalkmute}{HTML}{5F6E73}
\definecolor{overduedeep}{HTML}{8B3415}
@COLORDEFS@
\color{chalk}
\setlength\parindent{0pt}
\pagestyle{empty}
\newcommand\stagedot[1]{\textcolor{#1}{\rule[0.1ex]{1.6ex}{1.6ex}}}
\newcommand\chip[3]{\mbox{\stagedot{#1}\hspace{3pt}{\footnotesize\color{chalkdim}#2 \textbf{\color{chalk}#3}}}}
\newcommand\district[2]{\vspace{14pt}{\display\LARGE\bfseries #1}\hspace{6pt}{\ttfamily\small\color{chalkdim}#2 venues}\par\vspace{2pt}\textcolor{chalk}{\rule{\linewidth}{1.2pt}}\par\vspace{4pt}}
\newcommand\stagehead[3]{\vspace{8pt}{\display\large\bfseries\stagedot{#1}\hspace{5pt}#2\hspace{5pt}{\mdseries\color{chalkdim}#3}}\par\vspace{2pt}}
\newenvironment{venue}{\par\begin{minipage}{\linewidth}\vspace{4pt}}{\vspace{3pt}\par\textcolor{chalkmute}{\rule{\linewidth}{0.3pt}}\end{minipage}\par}
\newcommand\venuename[3]{{\display\normalsize\bfseries #1}\hspace{5pt}\fbox{\scriptsize\ttfamily\color{chalkdim}#2}\par\vspace{1pt}}
\newcommand\venuemeta[1]{{\ttfamily\footnotesize\color{chalkdim}#1}\par}
\newcommand\venueflags[1]{{\ttfamily\footnotesize\color{chalkmute}#1}\par}
\newcommand\venueact[1]{{\small $\rightarrow$ #1}\par}
\newcommand\venueactod[1]{{\small\color{overduedeep}$\rightarrow$ #1}\par}
\newcommand\venuelog[2]{{\footnotesize{\ttfamily\color{chalkdim}#1} --- \color{chalkdim}#2}\par}
\newcommand\row[4]{{\ttfamily\footnotesize #1} & #2 & {\ttfamily\footnotesize #3} & #4 \\}
\newcommand\rowod[4]{{\ttfamily\footnotesize\color{overduedeep}\textbf{#1 !}} & #2 & {\ttfamily\footnotesize #3} & \textcolor{overduedeep}{#4} \\}
\setlength\fboxsep{2pt}
\begin{document}

{\display\Huge\bfseries LUDI}\hspace{10pt}{\ttfamily\small\color{chalkdim}Cyprus venue atlas --- pipeline brief}\hfill{\ttfamily\small\color{chalkdim}@DATE@}\par
\vspace{3pt}\textcolor{chalk}{\rule{\linewidth}{2pt}}\par
\vspace{8pt}
{\display\Large @NVEN@ venues · \textcolor{slive}{\textbf{@NLIVE@ live}} · \textcolor{overduedeep}{@NOD@ overdue}}\par
\vspace{6pt}
@CHIPS@\par
\vspace{6pt}
{\small Live map: \href{https://nikolasneofytou.github.io/ludi-atlas}{\ttfamily nikolasneofytou.github.io/ludi-atlas}\hspace{10pt}{\color{chalkmute}editor: append \ttfamily ?edit}}\par

\vspace{12pt}
{\display\LARGE\bfseries Next steps}\par\vspace{2pt}\textcolor{chalk}{\rule{\linewidth}{1.2pt}}\par
\begin{longtable}{@{}p{18mm}p{40mm}p{16mm}p{100mm}@{}}
{\scriptsize\ttfamily\color{chalkdim}BY} & {\scriptsize\ttfamily\color{chalkdim}VENUE} & {\scriptsize\ttfamily\color{chalkdim}OWNER} & {\scriptsize\ttfamily\color{chalkdim}ACTION} \\
\hline
\endhead
@NEXTROWS@
\end{longtable}

@BODY@

\vspace{10pt}
{\footnotesize\ttfamily\color{chalkmute}Generated @DATE@ from venues.json · source of truth: the ludi-atlas git repository · map: nikolasneofytou.github.io/ludi-atlas}

\end{document}
"""

if __name__ == "__main__":
    sys.exit(main())
