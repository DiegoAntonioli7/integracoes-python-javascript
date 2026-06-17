"""Gera gráficos SVG de benchmark a partir dos *_stats.csv do Locust."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "charts"

DATASETS = [
    ("REST", "Python", ROOT / "rest/results/rest_python_stats.csv"),
    ("REST", "JavaScript", ROOT / "rest/results/rest_javascript_stats.csv"),
    ("SOAP", "Python", ROOT / "soap/results/soap_python_stats.csv"),
    ("SOAP", "JavaScript", ROOT / "soap/results/soap_javascript_stats.csv"),
    ("GraphQL", "Python", ROOT / "graphql/results/graphql_python_stats.csv"),
    ("GraphQL", "JavaScript", ROOT / "graphql/results/graphql_javascript_stats.csv"),
]

PROTOCOLS = ["REST", "SOAP", "GraphQL"]
COLORS = {"Python": "#2563eb", "JavaScript": "#f59e0b"}
WIDTH, HEIGHT = 920, 480
MARGIN_LEFT, MARGIN_RIGHT = 72, 24
MARGIN_TOP, MARGIN_BOTTOM = 56, 88
CHART_W = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
CHART_H = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM


def load_aggregated(csv_path: Path) -> dict:
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) > 1 and row[1] == "Aggregated":
                return {
                    "avg_ms": float(row[5]),
                    "median_ms": float(row[4]),
                    "payload_bytes": float(row[8]),
                    "req_s": float(row[9]),
                }
    raise ValueError(f"Linha Aggregated não encontrada em {csv_path}")


def collect_metrics() -> dict:
    metrics = {}
    for protocol, lang, path in DATASETS:
        metrics[(protocol, lang)] = load_aggregated(path)
    return metrics


def nice_max(value: float, steps: int = 5) -> float:
    if value <= 0:
        return 1
    raw = value * 1.12
    magnitude = 10 ** (len(str(int(raw))) - 1)
    return ((int(raw / magnitude) + 1) * magnitude) if raw > magnitude else raw


def svg_text(x, y, text, size=13, anchor="start", weight="normal", fill="#1f2937"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="system-ui,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{text}</text>'
    )


def draw_grouped_bars(
    title: str,
    y_label: str,
    values: dict,
    value_fn,
    format_fn,
    filename: str,
    y_max: float | None = None,
):
    if y_max is None:
        y_max = max(value_fn(metrics) for metrics in values.values())
    y_max = nice_max(y_max)

    bars = []
    grid = []
    n_groups = len(PROTOCOLS)
    group_width = CHART_W / n_groups
    bar_width = group_width * 0.28
    gap = group_width * 0.08

    for i in range(6):
        y = MARGIN_TOP + CHART_H * i / 5
        val = y_max * (1 - i / 5)
        grid.append(f'<line x1="{MARGIN_LEFT}" y1="{y:.1f}" x2="{WIDTH - MARGIN_RIGHT}" y2="{y:.1f}" stroke="#e5e7eb" stroke-width="1"/>')
        grid.append(svg_text(MARGIN_LEFT - 8, y + 4, format_fn(val), size=11, anchor="end"))

    for gi, protocol in enumerate(PROTOCOLS):
        cx = MARGIN_LEFT + group_width * gi + group_width / 2
        for li, lang in enumerate(["Python", "JavaScript"]):
            val = value_fn(values[(protocol, lang)])
            h = (val / y_max) * CHART_H if y_max else 0
            x = cx - bar_width - gap / 2 + li * (bar_width + gap)
            y = MARGIN_TOP + CHART_H - h
            color = COLORS[lang]
            bars.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{h:.1f}" '
                f'fill="{color}" rx="3"/>'
            )
            if h > 18:
                bars.append(svg_text(x + bar_width / 2, y + 14, format_fn(val), size=10, anchor="middle", fill="#fff", weight="600"))
        bars.append(svg_text(cx, HEIGHT - MARGIN_BOTTOM + 28, protocol, size=13, anchor="middle", weight="600"))

    legend_x = MARGIN_LEFT
    legend = []
    for li, lang in enumerate(["Python", "JavaScript"]):
        lx = legend_x + li * 130
        legend.append(f'<rect x="{lx}" y="18" width="14" height="14" fill="{COLORS[lang]}" rx="2"/>')
        legend.append(svg_text(lx + 20, 30, lang, size=12))

    svg = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
            '<rect width="100%" height="100%" fill="#ffffff"/>',
            svg_text(MARGIN_LEFT, 32, title, size=16, weight="600"),
            svg_text(MARGIN_LEFT, HEIGHT - 14, y_label, size=11, fill="#6b7280"),
            *legend,
            f'<line x1="{MARGIN_LEFT}" y1="{MARGIN_TOP + CHART_H}" x2="{WIDTH - MARGIN_RIGHT}" y2="{MARGIN_TOP + CHART_H}" stroke="#9ca3af" stroke-width="1"/>',
            *grid,
            *bars,
            "</svg>",
        ]
    )
    out = OUT_DIR / filename
    out.write_text(svg, encoding="utf-8")
    print(f"Gerado: {out}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics = collect_metrics()

    draw_grouped_bars(
        "Tempo médio de resposta (Aggregated)",
        "Milissegundos (ms)",
        metrics,
        lambda m: m["avg_ms"],
        lambda v: f"{v:.1f}",
        "response_time.svg",
    )

    draw_grouped_bars(
        "Tamanho médio do payload (Aggregated)",
        "Kilobytes (KB)",
        metrics,
        lambda m: m["payload_bytes"] / 1024,
        lambda v: f"{v:.1f}",
        "payload_size.svg",
    )

    draw_grouped_bars(
        "Throughput (Aggregated)",
        "Requisições por segundo (req/s)",
        metrics,
        lambda m: m["req_s"],
        lambda v: f"{v:.1f}",
        "throughput.svg",
    )


if __name__ == "__main__":
    main()
