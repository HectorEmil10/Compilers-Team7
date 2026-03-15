import re
from pathlib import Path


class Lexer:
    def __init__(self, lexemes, resource_dir: str):
        # Main lexer variables
        self.lexemes = lexemes
        self.resource_dir = Path(resource_dir)
        self.keywords = set()
        self.token_classification = {}
        self.total_tokens = 0

        # Create token categories
        self.token_classification["Keywords"] = set()
        self.token_classification["Identifiers"] = set()
        self.token_classification["Operators"] = set()
        self.token_classification["Punctuation"] = set()
        self.token_classification["Constants"] = set()
        self.token_classification["Literals"] = set()
        self.token_classification["Unknown"] = set()

        # Load resource files
        self._load_keywords()
        self._load_tokens()

    def _load_keywords(self):
        keywords_path = self.resource_dir / "keywords.txt"

        if keywords_path.exists():
            with open(keywords_path, "r", encoding="utf-8") as file:
                for line in file:
                    word = line.strip()
                    if word:
                        self.keywords.add(word)

    def _load_tokens(self):
        tokens_path = self.resource_dir / "tokens.txt"

        if tokens_path.exists():
            with open(tokens_path, "r", encoding="utf-8") as file:
                for line in file:
                    token_name = line.strip()
                    if token_name and token_name not in self.token_classification:
                        self.token_classification[token_name] = set()

    def create_keyword_regex(self):
        if not self.keywords:
            return r"$^"  # regex that matches nothing

        regex_creator = "|".join(sorted(self.keywords))
        return rf"\b({regex_creator})\b"

    def tokenize(self):
        keyword_regex = self.create_keyword_regex()

        # Regex patterns used in the project
        id_regex = r"[a-zA-Z_][a-zA-Z0-9_]*"

        op_regex = (
            r">>=|<<=|\+=|-=|\*=|/=|%=|==|!=|>=|<=|&&|\|\||\+\+|--|<<|>>|"
            r"&=|\|=|\^=|=|>|<|!|~|\+|-|\*|/|%|&|\||\^|\?|:"
        )

        # # is treated as punctuation only during preprocessing
        punt_regex = r"\.\.\.|[()\[\]{};,.:]"

        const_regex = (
            r"(0[xX][0-9a-fA-F]+)"
            r"|(0[0-7]+)"
            r"|(0|[1-9][0-9]*)"
            r"|(([0-9]+\.[0-9]+([eE][+-]?[0-9]+)?)"
            r"|(\.[0-9]+([eE][+-]?[0-9]+)?)"
            r"|([0-9]+[eE][+-]?[0-9]+))"
            r"|('([^'\\]|\\.)')"
        )

        lit_regex = r'"([^"\\]|\\.)*"'

        # Pattern used to scan tokens in a line
        token_pattern = re.compile(
            rf"{lit_regex}"
            rf"|{const_regex}"
            rf"|{op_regex}"
            rf"|{punt_regex}"
            rf"|{id_regex}"
            rf"|#"
            rf"|[^\s]+"
        )

        # Go through all lexemes
        for i in range(len(self.lexemes)):
            lexeme = str(self.lexemes[i])

            # Remove single line comments
            cleared_lexeme = re.sub(r"//.*", "", lexeme).strip()

            if not cleared_lexeme:
                self.lexemes[i] = "\n"
                continue
            else:
                self.lexemes[i] = cleared_lexeme

            # Check if the line starts with #
            preprocessing_line = cleared_lexeme.lstrip().startswith("#")

            # Remove literals so the rest can be classified (same idea as Java version)
            no_lit_lexeme = re.sub(lit_regex, "", cleared_lexeme).strip()

            # Classify tokens by category
            self.classify_and_count(id_regex, no_lit_lexeme, "Identifiers")
            self.classify_and_count(keyword_regex, no_lit_lexeme, "Keywords")
            self.classify_and_count(op_regex, no_lit_lexeme, "Operators")
            self.classify_and_count(punt_regex, no_lit_lexeme, "Punctuation")
            self.classify_and_count(const_regex, no_lit_lexeme, "Constants")
            self.classify_and_count(lit_regex, cleared_lexeme, "Literals")

            # Handle # depending on the rule
            if "#" in cleared_lexeme:
                if preprocessing_line:
                    self.token_classification["Punctuation"].add("#")
                    self.total_tokens += 1
                else:
                    self.token_classification["Unknown"].add("#")
                    self.total_tokens += 1

            # Look for unknown tokens by scanning one by one
            matches = list(token_pattern.finditer(cleared_lexeme))
            consumed = []

            for match in matches:
                token = match.group()

                if token == "#":
                    consumed.append((match.start(), match.end()))
                    continue

                if (
                    re.fullmatch(lit_regex, token)
                    or re.fullmatch(const_regex, token)
                    or re.fullmatch(op_regex, token)
                    or re.fullmatch(punt_regex, token)
                    or re.fullmatch(id_regex, token)
                ):
                    consumed.append((match.start(), match.end()))

            # Build fragments that were not recognized
            unknown_chars = [True] * len(cleared_lexeme)

            for start, end in consumed:
                for j in range(start, end):
                    unknown_chars[j] = False

            unknown_buffer = []
            for idx, ch in enumerate(cleared_lexeme):
                if unknown_chars[idx] and not ch.isspace():
                    unknown_buffer.append(ch)
                elif unknown_buffer:
                    unknown_token = "".join(unknown_buffer).strip()
                    if unknown_token:
                        self.token_classification["Unknown"].add(unknown_token)
                        self.total_tokens += 1
                    unknown_buffer = []

            if unknown_buffer:
                unknown_token = "".join(unknown_buffer).strip()
                if unknown_token:
                    self.token_classification["Unknown"].add(unknown_token)
                    self.total_tokens += 1

        return self.token_classification

    def classify_and_count(self, regex, text, category):
        pattern = re.compile(regex)
        matches = pattern.finditer(text)

        for match in matches:
            token = match.group()

            # Make sure keywords are not counted as identifiers
            if category == "Identifiers":
                if token not in self.keywords:
                    self.token_classification[category].add(token)
                    self.total_tokens += 1

            elif category == "Keywords":
                if token in self.keywords:
                    self.token_classification[category].add(token)
                    self.total_tokens += 1

            else:
                self.token_classification[category].add(token)
                self.total_tokens += 1

    def get_total_tokens(self):
        return self.total_tokens