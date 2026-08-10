# pages/mentoria.py
#
# Página dedicada à mentoria (produto independente do relatório).
# Paleta/fontes/header/footer agora vêm de pages/layout.py — não redeclare
# tokens aqui. Se quiser mudar cor ou fonte do site, mexe em layout.py, não
# nesta página.
#
# Pendências de conteúdo (procure "PLACEHOLDER" na renderização):
#   - Foto do Gustavo: src aponta pra "/assets/gushero.jpg" — assumindo que
#     o mount estático segue o mesmo padrão usado em about.py pro
#     "gustavo.jpg" (frontend/assets/, servido em /assets). Se o mount real
#     for outro (ex: /static/), corrigir o path abaixo. Coloque o arquivo
#     físico gushero.jpg em frontend/assets/ antes de considerar isso pronto.
#   - 2-3 depoimentos ou casos de sucesso reais (seção de prova social)

from nicegui import ui
from pages.layout import design_tokens, site_header, site_footer

MENTORSHIP_TIERS = [
    {
        "name": "Básico",
        "price": "2.000",
        "tier_key": "mentoria_basico",
        "features": [
            "10 encontros",
            "Acompanhamento em 1 processo de aplicação",
            "Auxílio para a composição do currículo",
            "Auxílio para a escrita do statement of purpose",
            "Análise do departamento",
            "Análise de 1 professor",
        ],
    },
    {
        "name": "Intermediário",
        "price": "2.250",
        "tier_key": "mentoria_intermediario",
        "features": [
            "12 encontros",
            "Acompanhamento em dois processos de aplicação",
            "Auxílio para a composição do currículo",
            "Auxílio para a escrita do statement of purpose",
            "Auxílio para a escrita do projeto",
            "Análise do departamento",
            "Análise de 1 professor",
        ],
        "highlight": True,
    },
    {
        "name": "Avançado",
        "price": "2.500",
        "tier_key": "mentoria_avancado",
        "features": [
            "14 encontros",
            "Acompanhamento em três processos de aplicação",
            "Auxílio para a composição do currículo",
            "Auxílio para a escrita do statement of purpose",
            "Análise do departamento",
            "Análise de 1 professor",
        ],
    },
]

PROCESS_STEPS = [
    (
        "Apresentação da dinâmica",
        "Como funciona o processo seletivo de pós-graduação no Canadá e "
        "alinhamento da estratégia com o seu perfil e objetivos.",
    ),
    (
        "Preparação documental e textual",
        "Carta de motivação, currículo acadêmico e demais documentos "
        "exigidos, revisados e estruturados etapa por etapa.",
    ),
    (
        "Identificação de departamentos e supervisores",
        "Mapeamento de programas e potenciais orientadores compatíveis "
        "com sua linha de pesquisa.",
    ),
    (
        "Estratégias de contato e engajamento",
        "Como abordar supervisores e departamentos de forma que gere "
        "resposta, não silêncio.",
    ),
]


def mentoria_page() -> None:
    design_tokens()

    with ui.column().classes("w-full min-h-screen bg-[#F5F0E6] font-body"):

        site_header("mentoria")

        # hero
        with ui.column().classes("w-full items-center py-20 px-4"):
            with ui.column().classes(
                "max-w-2xl w-full bg-white border hairline rounded-none shadow-sm "
                "p-10 gap-4 items-start"
            ):
                ui.label("Mentoria para sua pós-graduação").classes(
                    "font-display text-4xl font-semibold text-[#16233D] leading-tight"
                )
                ui.label(
                    "Acompanhamento individual, de ponta a ponta, no processo de "
                    "aplicação — decisões embasadas no seu perfil, não em achismo "
                    "de fórum de imigração."
                ).classes("text-[#4B5563] text-base leading-relaxed max-w-lg")
                ui.button(
                    "Ver planos",
                    on_click=lambda: ui.run_javascript(
                        "document.getElementById('planos-mentoria')"
                        ".scrollIntoView({behavior:'smooth'})"
                    ),
                ).classes(
                    "bg-[#A6402F] text-[#F5F0E6] rounded-none px-7 py-2.5 mt-2 "
                    "font-mono text-xs tracking-wide hover:bg-[#8a3327]"
                )

        # o que é
        with ui.column().classes("w-full items-center py-16 px-4 bg-white"):
            with ui.column().classes("max-w-3xl gap-4"):
                ui.label("O que é a mentoria").classes(
                    "font-display text-3xl font-semibold text-[#16233D] mb-1"
                )
                ui.label(
                    "A mentoria é composta de reuniões preparatórias para a candidatura. "
                    "Com elas, você entende o processo seletivo de pós-graduação no "
                    "Canadá em detalhe — editais, prazos, critérios de avaliação, "
                    "documentação exigida por universidade e departamento. A mentoria "
                    "desmistifica etapas que costumam travar o candidato (carta de "
                    "motivação, currículo acadêmico, contato com potenciais "
                    "orientadores) e ajuda a organizar ideias e documentos de forma "
                    "estruturada. O objetivo é fazer a candidatura de forma "
                    "inteligente, com decisões embasadas em cima do seu perfil e "
                    "objetivos acadêmicos."
                ).classes("text-[#4B5563] leading-relaxed")

        # para quem é
        with ui.column().classes("w-full items-center py-16 px-4"):
            with ui.column().classes("max-w-3xl gap-4"):
                ui.label("Para quem é").classes(
                    "font-display text-3xl font-semibold text-[#16233D] mb-1"
                )
                for item in [
                    "Para quem decidiu fazer uma pós no Canadá",
                    "Para quem quer realmente entender o processo seletivo",
                    "Para quem quer tomar as melhores decisões durante a aplicação",
                ]:
                    with ui.row().classes("items-start gap-3"):
                        ui.label("—").classes("text-[#A6402F] font-mono")
                        ui.label(item).classes("text-[#4B5563] leading-relaxed")
 # bio do mentor
        with ui.column().classes("w-full items-center py-16 px-4"):
            with ui.row().classes(
                "max-w-3xl w-full gap-8 items-center flex-wrap justify-center"
            ):
                ui.image("/assets/gstvhero.jpg").classes(
                    "w-40 h-40 rounded-full object-cover border hairline flex-shrink-0"
                )
                with ui.column().classes("gap-2 max-w-md"):
                    ui.label("Consultor principal").classes(
                        "font-mono text-xs tracking-widest text-[#A6402F]"
                    )
                    ui.label(
                        "Gustavo Denani é candidato a Ph.D. em Antropologia pela "
                        "Universidade de Ottawa. Morou em Ottawa e Montreal entre "
                        "2021 e 2024, período em que adquiriu experiência prática "
                        "em processos seletivos e editais de bolsa. Passou pelo "
                        "processo de seleção sozinho e, apesar do resultado "
                        "positivo, hoje reconhece os erros cometidos e as decisões "
                        "que teria tomado com a experiência que tem agora. É dessa "
                        "vivência que nasce a mentoria: tornar sua candidatura não "
                        "apenas possível, mas inteligente e segura."
                    ).classes("text-[#4B5563] text-sm leading-relaxed")

        # como funciona — numeração real (sequência de fato)
        with ui.column().classes("w-full items-center py-16 px-4 bg-white"):
            with ui.column().classes("max-w-3xl gap-6 w-full"):
                ui.label("Como funciona").classes(
                    "font-display text-3xl font-semibold text-[#16233D] mb-1"
                )
                for i, (title, desc) in enumerate(PROCESS_STEPS, start=1):
                    with ui.row().classes(
                        "flex-nowrap gap-4 items-start py-4 w-full "
                        "border-b hairline last:border-b-0"
                    ):
                        ui.label(f"{i:02d}").classes(
                            "font-mono text-lg text-[#A6402F] w-10 flex-shrink-0"
                        )
                        with ui.column().classes("gap-1 flex-1 min-w-0"):
                            ui.label(title).classes("text-[#16233D] font-semibold")
                            ui.label(desc).classes(
                                "text-[#4B5563] text-sm leading-relaxed"
                            )

        # planos
        with ui.column().classes(
            "w-full items-center py-16 px-4 bg-[#16233D]"
        ).props('id="planos-mentoria"'):
            ui.label("Escolha seu plano de mentoria").classes(
                "font-display text-3xl font-semibold text-[#F5F0E6] mb-2 text-center"
            )
            ui.label(
                "Todos os planos incluem encontros agendados conforme sua "
                "disponibilidade."
            ).classes("text-[#F5F0E6]/60 mb-10 text-center font-mono text-sm")

            with ui.row().classes("gap-6 flex-wrap justify-center"):
                for tier in MENTORSHIP_TIERS:
                    highlight = tier.get("highlight", False)
                    card_classes = (
                        "w-72 p-6 rounded-none flex flex-col gap-3 bg-[#F5F0E6] "
                        "border-2 border-[#A6402F]"
                        if highlight
                        else "w-72 p-6 rounded-none flex flex-col gap-3 bg-[#F5F0E6]"
                    )
                    with ui.card().classes(card_classes):
                        if highlight:
                            ui.label("MAIS PROCURADO").classes(
                                "text-[10px] font-mono tracking-widest text-[#F5F0E6] "
                                "bg-[#A6402F] px-3 py-1 self-start"
                            )
                        ui.label(tier["name"]).classes(
                            "font-display text-xl font-semibold text-[#16233D] mt-1"
                        )
                        with ui.row().classes("items-baseline gap-1"):
                            ui.label("R$").classes("font-mono text-sm text-[#A6402F]")
                            ui.label(tier["price"]).classes(
                                "font-mono text-3xl font-medium text-[#A6402F]"
                            )

                        ui.element("div").classes("h-px w-full bg-[#B8925A55] my-2")

                        for feature in tier["features"]:
                            with ui.row().classes("items-center gap-2 flex-nowrap"):
                                ui.label("✓").classes(
                                    "text-[#A6402F] font-mono text-xs flex-shrink-0"
                                )
                                ui.label(feature).classes(
                                    "text-[#4B5563] text-xs leading-snug"
                                )

                        ui.space()

                        def make_handler(t=tier["tier_key"]):
                            def handler():
                                ui.navigate.to(f"/mentoria/cadastro?tier={t}")
                            return handler

                        ui.button(
                            "Quero este plano",
                            on_click=make_handler(),
                        ).classes(
                            "w-full mt-2 bg-[#16233D] text-[#F5F0E6] rounded-none "
                            "py-2 font-mono text-xs tracking-wide hover:bg-[#0f182b]"
                        )

        site_footer()
