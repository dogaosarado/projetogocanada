# pages/about.py
#
# Paleta/fontes/header/footer vêm de pages/layout.py.

from nicegui import ui
from pages.layout import design_tokens, site_header, site_footer


def about_page() -> None:
    design_tokens()

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):

        site_header("quem-somos")

        with ui.column().classes("w-full items-center py-20 px-4"):
            with ui.column().classes("w-full max-w-2xl gap-6"):
                ui.label("01").classes("font-mono text-sm text-[#A6402F]")
                ui.label("Quem somos").classes(
                    "font-display text-4xl font-semibold text-[#16233D] mb-2"
                )

                ui.label(
                    "A GoCanadaBR nasceu para ajudar estudantes brasileiros a fazerem sua "
                    "pós-graduação no Canadá. Com informação e estratégia, construímos "
                    "uma candidatura competitiva, tornando compreensível cada etapa da aplicação."
                ).classes("text-[#4B5563] text-lg leading-relaxed")

                ui.label(
                    "Fazemos o levantamento detalhado de universidades, programas, professores "
                    "e prazos, para que você possa investir seu tempo na candidatura em si — "
                    "não em garimpar informação espalhada em dezenas de sites."
                ).classes("text-[#4B5563] text-lg leading-relaxed")

                ui.label(
                    "Trabalhamos com pesquisa individualizada por plano contratado: quanto mais "
                    "aprofundado o plano, mais universidades, professores e contexto de pesquisa "
                    "entregamos por candidatura."
                ).classes("text-[#4B5563] text-lg leading-relaxed")

        with ui.column().classes("w-full items-center py-20 px-4 bg-white"):
            with ui.column().classes("w-full max-w-2xl gap-6"):
                ui.label("02").classes("font-mono text-sm text-[#A6402F]")
                ui.label("Consultor").classes(
                    "font-display text-4xl font-semibold text-[#16233D] mb-2"
                )

                with ui.row().classes("w-full gap-8 items-center flex-wrap"):
                    ui.image("/assets/gustavo.jpg").classes(
                        "w-48 h-48 rounded-none object-cover shadow-md flex-shrink-0"
                    )

                ui.label(
                    "Olá! Meu nome é Gustavo Denani e sou candidato de Ph.D em Antropologia pela Universidade de "
                    "Ottawa. Morei em Ottawa e em Montreal durante 2021 e 2024, durante o doutorado adquiri experiência "
                    "em processos seletivos e editais de bolsa. Passei pelo processo de seleção sozinho, e apesar de ter "
                    "sido bem sucedido, hoje entendo os erros que cometi nessa etapa e as decisões que eu teria tomado "
                    "caso eu tivesse experiência. É dessa experiência que consigo fazer do seu objetivo um projeto "
                    "não somente possível, mas de modo inteligente e com confiança."
                ).classes("text-[#4B5563] text-lg leading-relaxed")

                with ui.row().classes("gap-6"):
                    ui.link(
                        "LinkedIn",
                        "https://www.linkedin.com/in/gustavo-denani-894978262/",
                        new_tab=True,
                    ).classes("text-[#A6402F] font-mono text-sm hover:text-[#8a3327]")
                    ui.link(
                        "Currículo Lattes",
                        "https://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=K4247833Y7",
                        new_tab=True,
                    ).classes("text-[#A6402F] font-mono text-sm hover:text-[#8a3327]")

                ui.button(
                    "Ver planos", on_click=lambda: ui.navigate.to("/#planos")
                ).classes(
                    "bg-[#A6402F] text-[#F5F0E6] rounded-none px-6 py-2.5 mt-4 "
                    "font-mono text-xs tracking-wide hover:bg-[#8a3327] w-fit"
                )

        site_footer()
