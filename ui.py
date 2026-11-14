"""
UI Helper: ANSI color & formatting untuk CLI responsive.
"""

import shutil

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"

BOX_TL = "┌"
BOX_TR = "┐"
BOX_BL = "└"
BOX_BR = "┘"
BOX_H = "─"
BOX_V = "│"
BOX_T = "┬"
BOX_B = "┴"
BOX_L = "├"
BOX_R = "┤"
BOX_X = "┼"


def _term_width() -> int:
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(v, hi))


def _calc_widths(cols: list, rows: list, min_w: int = 4, max_total: int = None) -> list:
    """Hitung lebar kolom optimal berdasarkan header + data, fit ke terminal."""
    if max_total is None:
        max_total = _term_width() - 4  # border kiri/kanan + margin
    n = len(cols)
    # minimal per kolom
    widths = [min_w] * n
    # header
    for i, c in enumerate(cols):
        widths[i] = max(widths[i], len(str(c)))
    # data rows
    for row in rows:
        for i, v in enumerate(row):
            widths[i] = max(widths[i], len(str(v)))
    # padding 2 spasi per kolom (kiri+kanan)
    total = sum(w + 2 for w in widths) + (n + 1)  # + border chars
    if total <= max_total:
        return widths
    # perlu shrink: kurangi dari kolom terbesar dulu
    while total > max_total:
        # cari kolom yang bisa dikurangi (lebih dari min_w)
        idx = -1
        max_w = min_w
        for i, w in enumerate(widths):
            if w > min_w and w > max_w:
                max_w = w
                idx = i
        if idx == -1:
            break
        widths[idx] -= 1
        total = sum(w + 2 for w in widths) + (n + 1)
    return widths


def header(text: str, width: int = None) -> str:
    """Header box responsive."""
    if width is None:
        width = _clamp(len(text) + 4, 40, _term_width())
    lines = [
        f"{CYAN}{BOX_TL}{BOX_H * (width - 2)}{BOX_TR}{RESET}",
        f"{CYAN}{BOX_V}{RESET}{f' {text} '.center(width - 2)}{CYAN}{BOX_V}{RESET}",
        f"{CYAN}{BOX_BL}{BOX_H * (width - 2)}{BOX_BR}{RESET}",
    ]
    return "\n".join(lines)


def sub_header(text: str, width: int = None) -> str:
    """Sub-header box responsive."""
    if width is None:
        width = _clamp(len(text) + 4, 36, _term_width())
    lines = [
        f"{BLUE}{BOX_L}{BOX_H * (width - 2)}{BOX_R}{RESET}",
        f"{BLUE}{BOX_V}{RESET}{f' {text} '.center(width - 2)}{BLUE}{BOX_V}{RESET}",
        f"{BLUE}{BOX_BL}{BOX_H * (width - 2)}{BOX_BR}{RESET}",
    ]
    return "\n".join(lines)


def menu_box(title: str, options: list, width: int = None) -> str:
    """Kotak menu responsive."""
    content_width = max(len(title), max((len(f"{i}. {o}") for i, o in enumerate(options, 1)), default=0), len("0. Kembali"))
    if width is None:
        width = _clamp(content_width + 4, 36, _term_width())
    lines = [f"{CYAN}{BOX_TL}{BOX_H * (width - 2)}{BOX_TR}{RESET}"]
    if title:
        lines.append(f"{CYAN}{BOX_V}{RESET}{f' {title} '.ljust(width - 2)}{CYAN}{BOX_V}{RESET}")
        lines.append(f"{CYAN}{BOX_L}{BOX_H * (width - 2)}{BOX_R}{RESET}")
    for i, opt in enumerate(options, 1):
        content = f"{i}. {opt}".ljust(width - 2)
        lines.append(f"{CYAN}{BOX_V}{RESET}{content}{CYAN}{BOX_V}{RESET}")
    content0 = f"0. Kembali".ljust(width - 2)
    lines.append(f"{CYAN}{BOX_V}{RESET}{content0}{CYAN}{BOX_V}{RESET}")
    lines.append(f"{CYAN}{BOX_BL}{BOX_H * (width - 2)}{BOX_BR}{RESET}")
    return "\n".join(lines)


def info(msg: str) -> str:
    return f"{BLUE}ℹ{RESET} {msg}"


def success(msg: str) -> str:
    return f"{GREEN}✓{RESET} {msg}"


def warning(msg: str) -> str:
    return f"{YELLOW}⚠{RESET} {msg}"


def error(msg: str) -> str:
    return f"{RED}✗{RESET} {msg}"


def input_prompt(label: str) -> str:
    return f"{CYAN}▸{RESET} {label}: "


def confirm_prompt(msg: str) -> str:
    return f"{YELLOW}?{RESET} {msg} (y/n): "


def sort_kriteria_menu() -> str:
    return menu_box("", [
        "Nama (A-Z)",
        "NIM (terkecil)",
        "IPK (tertinggi)"
    ])


def sort_arah_menu() -> str:
    return menu_box("", [
        "Naik (Ascending)",
        "Turun (Descending)"
    ])


def main_menu() -> str:
    return menu_box("", [
        "Data Mahasiswa",
        "Data Mata Kuliah",
        "Input Nilai",
        "Lihat IPK",
        "Absensi",
        "Cari & Urutkan"
    ])


def submenu_mahasiswa() -> str:
    return menu_box("DATA MAHASISWA", [
        "Lihat Semua",
        "Tambah",
        "Ubah",
        "Hapus"
    ])


def submenu_matakuliah() -> str:
    return menu_box("DATA MATA KULIAH", [
        "Lihat Semua",
        "Tambah",
        "Ubah",
        "Hapus"
    ])


def submenu_absensi() -> str:
    return menu_box("ABSENSI", [
        "Input Absensi",
        "Rekap Kehadiran"
    ])


def submenu_cari_urut() -> str:
    return menu_box("CARI & URUTKAN", [
        "Cari Mahasiswa",
        "Urutkan Mahasiswa"
    ])


def draw_table(cols: list, rows: list, color_fn=None) -> str:
    """Gambar tabel responsive penuh. color_fn(row_idx) -> color string atau None."""
    if not rows:
        return empty_state("Data kosong.")
    widths = _calc_widths(cols, rows)
    n = len(cols)
    # header
    head = f"{BOX_TL}"
    for i, w in enumerate(widths):
        head += f"{BOX_H * (w + 2)}"
        head += f"{BOX_T if i < n - 1 else BOX_TR}"
    hdr_row = f"{BOX_V}{BOX_V.join([f' {c:<{w}} ' for c, w in zip(cols, widths)])}{BOX_V}"
    sep = f"{BOX_L}"
    for i, w in enumerate(widths):
        sep += f"{BOX_H * (w + 2)}"
        sep += f"{BOX_X if i < n - 1 else BOX_R}"
    out = [f"{GRAY}{head}{RESET}", f"{BOLD}{hdr_row}{RESET}", f"{GRAY}{sep}{RESET}"]
    # data rows
    for ri, row in enumerate(rows):
        color = color_fn(ri) if color_fn else ""
        parts = []
        for i, (v, w) in enumerate(zip(row, widths)):
            s = str(v)
            if len(s) > w:
                s = s[:w - 1] + "…"
            parts.append(f" {s:<{w}} ")
        row_str = f"{BOX_V}{BOX_V.join(parts)}{BOX_V}"
        out.append(f"{color}{row_str}{RESET}" if color else row_str)
    # footer
    foot = f"{BOX_BL}"
    for i, w in enumerate(widths):
        foot += f"{BOX_H * (w + 2)}"
        foot += f"{BOX_B if i < n - 1 else BOX_BR}"
    out.append(f"{GRAY}{foot}{RESET}")
    return "\n".join(out)


def empty_state(msg: str = "Data kosong.") -> str:
    w = _clamp(len(msg) + 4, 30, _term_width())
    inner = f" {msg} ".center(w - 2)
    return (
        f"{GRAY}{BOX_TL}{BOX_H * (w - 2)}{BOX_TR}{RESET}\n"
        f"{GRAY}{BOX_V}{RESET}{inner}{GRAY}{BOX_V}{RESET}\n"
        f"{GRAY}{BOX_BL}{BOX_H * (w - 2)}{BOX_BR}{RESET}"
    )


# Backward compatibility
def table_header(cols: list, widths: list) -> str:
    head = f"{BOX_TL}"
    for i, w in enumerate(widths):
        head += f"{BOX_H * (w + 2)}"
        head += f"{BOX_T if i < len(widths) - 1 else BOX_TR}"
    row = f"{BOX_V}{BOX_V.join([f' {c:<{w}} ' for c, w in zip(cols, widths)])}{BOX_V}"
    sep = f"{BOX_L}"
    for i, w in enumerate(widths):
        sep += f"{BOX_H * (w + 2)}"
        sep += f"{BOX_X if i < len(widths) - 1 else BOX_R}"
    return f"{GRAY}{head}{RESET}\n{BOLD}{row}{RESET}\n{GRAY}{sep}{RESET}"


def table_row(vals: list, widths: list, color: str = "") -> str:
    parts = [f" {v:<{w}} " for v, w in zip(vals, widths)]
    row = f"{BOX_V}{BOX_V.join(parts)}{BOX_V}"
    return f"{color}{row}{RESET}" if color else row


def table_footer(widths: list) -> str:
    foot = f"{BOX_BL}"
    for i, w in enumerate(widths):
        foot += f"{BOX_H * (w + 2)}"
        foot += f"{BOX_B if i < len(widths) - 1 else BOX_BR}"
    return f"{GRAY}{foot}{RESET}"