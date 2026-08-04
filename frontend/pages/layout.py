# pages/layout.py
#
# Ponto único de verdade pra identidade visual do site: paleta, fontes,
# header e footer públicos. Nenhuma página deve declarar cor/fonte
# hardcoded fora daqui — se precisar de uma variação, ela nasce neste
# arquivo, não copiada e ajustada dentro de cada page.
#
# Uso em qualquer página pública:
#   design_tokens()          # uma vez, no topo da função da página
#   site_header("blog")      # "blog" = key ativa em NAV_ITEMS, pra grifar
#   ... conteúdo ...
#   site_footer()

from nicegui import ui
from state.user import get_name, is_logged_in, logout

# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------
COLORS = {
    "navy": "#16233D",
    "parchment": "#F5F0E6",
    "maple": "#A6402F",
    "maple_hover": "#8a3327",
    "gold": "#B8925A",
    "slate": "#4B5563",
}

# key, label, rota — ordem aqui é a ordem do menu em TODA página pública.
NAV_ITEMS = [
    ("mentoria", "Mentoria", "/"),
    ("relatorio", "Relatórios", "/relatorio"),
    ("quem-somos", "Quem somos", "/quem-somos"),
    ("blog", "Blog", "/blog"),
    ("contato", "Contato", "/contato"),
]


def design_tokens() -> None:
    """Injeta fontes e classes utilitárias. Idempotente o bastante pra
    chamar uma vez por página sem se preocupar."""
    ui.add_head_html(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
            .font-display { font-family: 'Fraunces', serif; }
            .font-body { font-family: 'Inter', sans-serif; }
            .font-mono { font-family: 'IBM Plex Mono', monospace; }
            .hairline { border-color: #B8925A55; }
            .seal {
                width: 64px; height: 64px; border-radius: 9999px;
                background: #A6402F; color: #F5F0E6;
                display: flex; align-items: center; justify-content: center;
                font-family: 'Fraunces', serif; font-weight: 700; font-size: 1.1rem;
                flex-shrink: 0;
            }
            /* Conteúdo de post de blog renderizado via ui.html() a partir de
               Markdown convertido — sem isso, h2/p/a saem no default cru do
               browser: título gigante, parágrafos colados, link sem cor. */
            .blog-content p {
                margin-bottom: 1.25rem;
                line-height: 1.7;
                color: #16233D;
            }
            .blog-content h2 {
                font-family: 'Fraunces', serif;
                font-size: 1.35rem;
                font-weight: 600;
                margin-top: 2rem;
                margin-bottom: 0.75rem;
                color: #16233D;
            }
            .blog-content h3 {
                font-family: 'Fraunces', serif;
                font-size: 1.15rem;
                font-weight: 600;
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                color: #16233D;
            }
            .blog-content a {
                color: #A6402F;
                text-decoration: underline;
                text-underline-offset: 2px;
            }
            .blog-content a:hover {
                color: #8a3327;
            }
        </style>
        """
    )


# ---------------------------------------------------------------------------
# Marca
# ---------------------------------------------------------------------------
def brand_logo() -> None:
    with ui.link(target="/").classes("flex items-center gap-2 no-underline"):
        ui.image("/assets/logo.svg").classes("w-9 h-9")
        ui.label("GoCanadaBR").classes(
            "font-display text-2xl font-semibold text-[#F5F0E6]"
        )


# ---------------------------------------------------------------------------
# Header público — antes cada página remontava o próprio nav (e cada uma
# tinha um subconjunto diferente de links — about.py não tinha "Mentoria"
# nem "Relatórios", blog.py não tinha nav nenhum). Agora é um componente
# só, com todos os links sempre, e destaque pra página ativa.
# ---------------------------------------------------------------------------
def site_header(active: str = "") -> None:
    with ui.row().classes(
        "w-full px-8 py-5 bg-[#16233D] justify-between items-center"
    ):
        brand_logo()
        with ui.row().classes("gap-1 items-center"):
            for key, label, route in NAV_ITEMS:
                classes = "font-mono text-xs tracking-wide px-3 py-2 rounded-none"
                if key == active:
                    classes += " text-[#F5F0E6] border-b-2 border-[#A6402F]"
                else:
                    classes += " text-[#F5F0E6]/70 hover:text-[#F5F0E6]"
                ui.button(
                    label, on_click=lambda r=route: ui.navigate.to(r)
                ).props("flat").classes(classes)
            ui.button("Entrar", on_click=lambda: ui.navigate.to("/login")).classes(
                "bg-[#A6402F] text-[#F5F0E6] rounded-none px-5 py-2 font-mono "
                "text-xs tracking-wide hover:bg-[#8a3327] ml-2"
            )


def site_footer() -> None:
    with ui.row().classes("w-full px-8 py-6 bg-[#16233D] justify-center"):
        ui.label("© 2026 GoCanada — Todos os direitos reservados").classes(
            "text-[#F5F0E6]/50 text-xs font-mono"
        )


# ---------------------------------------------------------------------------
# Header autenticado (painel etc.) — mesma paleta, escopo separado do
# público de propósito (usuário logado não precisa ver "Entrar").
# ---------------------------------------------------------------------------
def authenticated_header() -> None:
    if not is_logged_in():
        return
    with ui.row().classes(
        "w-full px-6 py-3 bg-[#16233D] justify-between items-center"
    ):
        brand_logo()
        name = get_name()
        ui.label(f"Bem-vindo(a), {name}" if name else "Bem-vindo(a)").classes(
            "text-[#F5F0E6]/80 font-mono text-sm"
        )
        with ui.row().classes("gap-3 items-center"):
            ui.button("Painel", on_click=lambda: ui.navigate.to("/painel")).props(
                "flat"
            ).classes("text-[#F5F0E6] font-mono text-xs")
            ui.button(
                "Sair",
                on_click=lambda: (logout(), ui.navigate.to("/login")),
            ).props("flat").classes("text-[#A6402F] font-mono text-xs")
