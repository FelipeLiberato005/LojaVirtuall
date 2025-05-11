import secrets

def gerar_chave_aleatoria(tamanho_em_bytes):
    """Gera uma chave aleatória em formato hexadecimal.

    Args:
        tamanho_em_bytes: O tamanho da chave em bytes.

    Returns:
        Uma string hexadecimal representando a chave.
    """
    return secrets.token_hex(tamanho_em_bytes)

# Exemplo: Gerar uma chave de 32 bytes (256 bits)
tamanho_chave = 16
chave_aleatoria = gerar_chave_aleatoria(tamanho_chave)
print(f"Chave aleatória: {chave_aleatoria}")


