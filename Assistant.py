class Assistant(object):

    def __init__(self) -> None:
        """
        """
        return None

    def get_help_message(self, text_list) -> str:
        """
        """
        wrap = 6
        head_text_0 = 'CRYPTO option:'
        content_text_0 = self.__box_print(text_list[0], wrap)
        head_text_1 = 'CURRENCY option:'
        content_text_1 = self.__box_print(text_list[1], wrap)
        head_text_ie = 'Please enter a 2-digit number(i.e: 01 or 10)\r\nFirst digit is CRYPTO\r\nSecond digit is CURRENCY'
        help_message = '\r\n'.join([head_text_0,
                                    content_text_0,
                                    head_text_1,
                                    content_text_1,
                                    head_text_ie])

        return help_message

    def __box_print(self, text, wrap=0) -> str:
        """
        """
        line_style = '-'
        paragraph = text.split('\n')
        if wrap > 0:
            index = 0
            while index < len(paragraph):
                paragraph[index] = self.__clean_line(paragraph[index])
                if len(paragraph[index]) > wrap:
                    paragraph = paragraph[:index] + \
                        self.__break_line(paragraph[index], wrap) + \
                        paragraph[index + 1:]
                index += 1

        length = (max([len(line) for line in paragraph]))

        box_list = list()
        frame = f'+{line_style * length}+'
        space = ' '
        for line in paragraph:
            box_list.append(f'|{line}{space * (length - len(line))}|')
        box_list.insert(0, frame)
        box_list.append(frame)
        box_str = '\r\n'.join(box_list)
        return box_str

    def __clean_line(self, text) -> str:
        """
        """
        if text[-1] == ' ':
            text = text[:-1]
        if text[0] == ' ':
            text = text[1:]
        return text

    def __break_line(self, text, wrap=80) -> (str, list):
        """
        """
        if len(text) > wrap:
            char = wrap
            while char > 0 and text[char] != ' ':
                char -= 1
            if char:
                text = [text[:char]] + self.__break_line(text[char + 1:], wrap)
            else:
                text = [text[:wrap - 1] + '-'] + \
                    self.__break_line(text[wrap - 1:], wrap)
            return text
        else:
            return [self.__clean_line(text)]


if __name__ == '__main__':
    # test
    text_list = ['0:BTC 1:ETH', '0:USD 1:JPY']
    assistant = Assistant()
    msg = assistant.get_help_message(text_list)
    print(msg)
