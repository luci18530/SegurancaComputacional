# patterns.py

SQL_INJECTION_PATTERNS = [
    r'(\bor\b|\band\b).*(=|like)',        # Uso de 'OR', 'AND' com operadores
    r'(\bunion\b|\bselect\b|\binsert\b|\bdelete\b|\bdrop\b)',  # Palavras-chave SQL
    r'(--|#)',                            # Comentários SQL
]

XSS_PATTERNS = [
    r'(<script.*?>.*?</script>)',         # Scripts HTML
    r'javascript:.*',                     # javascript URLs
    r'(\bon\w+?\s*=\s*".*?")',            # Atributos de evento em HTML
]

COMMAND_INJECTION_PATTERNS = [
    r'(;|\||\&\&|\|\|)\s*(cd|ls|echo|set|unset|export|cat|chmod|curl|wget|ping|netstat|ps|kill|uname|whoami|script|perl|python|ruby|bash|sh|sudo)\b',
    r'\b(exec|system|bash|sh|cmd|cat|ping|uname)\s*\('
]
