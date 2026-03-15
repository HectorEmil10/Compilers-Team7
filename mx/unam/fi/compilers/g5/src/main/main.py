from pathlib import Path
from lexer import Lexer


def read_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def print_results(tokens, total_tokens):
    if tokens["Unknown"]:
        print("Error: There are unrecognized tokens in the input.")
        print("Unknown tokens:", tokens["Unknown"])
        return

    for category, values in tokens.items():
        if category != "Unknown":
            print(f"{category}: {sorted(values)}")

    print(f"Total Tokens: {total_tokens}")


def main():
    resource_dir = Path(__file__).parent / "resources"

    print("Choose input method:")
    print("1. Type a string")
    print("2. Read from file")

    option = input("Option: ").strip()

    if option == "1":
        print("Write your code. Finish with an empty line:")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        text = "\n".join(lines)

    elif option == "2":
        filepath = input("Enter file path: ").strip()
        text = read_file(filepath)

    else:
        print("Invalid option.")
        return

    lexemes = text.split("\n")
    lexer = Lexer(lexemes, str(resource_dir))
    tokens = lexer.tokenize()

    print_results(tokens, lexer.get_total_tokens())


if __name__ == "__main__":
    main()