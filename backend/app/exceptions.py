from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo. Aguarde a confirmação do pagamento.",
        )


class NotFoundException(HTTPException):
    def __init__(self, resource: str = "Recurso"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} não encontrado.",
        )


class TierPermissionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seu plano não permite essa seleção.",
        )


class DuplicateRequestException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Você já enviou seu formulário de universidades. "
                "Para alterar suas escolhas, entre em contato com a equipe GoCanadaBR "
                "pelo contato@gocanadabr.com.br."
            ),
        )