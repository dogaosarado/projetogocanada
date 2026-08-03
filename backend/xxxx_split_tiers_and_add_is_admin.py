"""split tier enum into relatorio_*/mentoria_* and add is_admin

Revision ID: xxxx_split_tiers_and_add_is_admin
Revises: <7a1c9f3e2b44>
Create Date: 2026-07-30
"""
from alembic import op
import sqlalchemy as sa

# ATENÇÃO antes de rodar:
# 1. Preencha `down_revision` acima com o id da última revision existente
#    (rode `alembic heads` no seu projeto pra achar).
# 2. Renomeie este arquivo pra um revision id real gerado por
#    `alembic revision -m "split tier enum and add is_admin"` e cole este
#    conteúdo dentro, senão o alembic não vai reconhecer o arquivo.
# 3. Rode isso ANTES de trocar o código do modelo em produção — se o app
#    subir com o TierEnum novo mas o banco ainda tiver os valores antigos
#    ("basico", "intermediario", "avancado"), toda leitura de User quebra.
# 4. TESTE em staging/local primeiro. RENAME VALUE em enum Postgres é seguro
#    (não reescreve a tabela), mas é irreversível sem rodar o downgrade.

revision = "xxxx_split_tiers_and_add_is_admin"
down_revision = "<PREENCHER>"
branch_labels = None
depends_on = None


def upgrade():
    # Todo usuário existente foi criado quando só existia o produto
    # "relatório" — então os valores antigos mapeiam 1:1 pro prefixo
    # relatorio_*. Não existe usuário legado em "gratis" (tier não existia).
    op.execute("ALTER TYPE tierenum RENAME VALUE 'basico' TO 'relatorio_basico'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'intermediario' TO 'relatorio_intermediario'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'avancado' TO 'relatorio_avancado'")

    # novos valores
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'relatorio_gratis'")
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'mentoria_basico'")
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'mentoria_intermediario'")
    op.execute("ALTER TYPE tierenum ADD VALUE IF NOT EXISTS 'mentoria_avancado'")

    # is_admin — qualquer usuário que hoje está em relatorio_avancado E é
    # usado como conta de admin (ver `seu@email.com` nos dados de teste)
    # precisa virar is_admin=true manualmente depois desta migration.
    # Isso NÃO é inferível automaticamente: tier="avancado" hoje mistura
    # clientes reais do plano avançado com a(s) conta(s) de admin.
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="false"))


def downgrade():
    op.drop_column("users", "is_admin")
    # Não há downgrade seguro pra remover valores de enum Postgres
    # (ALTER TYPE ... DROP VALUE não existe nativamente). Se precisar
    # reverter de verdade, recrie o tipo do zero. Deixado assim de propósito
    # em vez de fingir um downgrade que não funciona.
    op.execute("ALTER TYPE tierenum RENAME VALUE 'relatorio_basico' TO 'basico'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'relatorio_intermediario' TO 'intermediario'")
    op.execute("ALTER TYPE tierenum RENAME VALUE 'relatorio_avancado' TO 'avancado'")
