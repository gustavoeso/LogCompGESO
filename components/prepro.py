class PrePro:
    @staticmethod
    def filter(source: str) -> str:
        import re
        # Remove comentarios no formato /* comentario */
        return re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
