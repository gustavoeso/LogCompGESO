class PrePro:
    @staticmethod
    def filter(source: str) -> str:
        import re
        # Remover comentários no formato /* comentário */
        return re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
