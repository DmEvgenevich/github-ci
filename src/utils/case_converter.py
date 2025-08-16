def camel_case_to_snake_case(input_str: str) -> str:
    chars = list()
    for char_index, char in enumerate(input_str):
        if char_index and char.isupper():
            next_index = char_index + 1
            flag = next_index >= len(input_str) or input_str[next_index].isupper()
            prev_char = input_str[char_index - 1]
            if prev_char.isupper() and flags:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)
