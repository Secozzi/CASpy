from collections import namedtuple

from PyQt5.Qt import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextBlockUserData, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit

ParenInfo = namedtuple("ParenInfo", "character position")
BracketInfo = namedtuple("BracketInfo", "character position")


class ParenMatchHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        block_data = TextBlockData()
        for pos, rune in enumerate(text):
            if rune in "()":
                block_data.parentheses.append(ParenInfo(rune, pos))
            if rune in "[]":
                block_data.brackets.append(BracketInfo(rune, pos))
        self.setCurrentBlockUserData(block_data)


class TextBlockData(QTextBlockUserData):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parentheses = []
        self.brackets = []


class TextEdit(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.highlighter = ParenMatchHighlighter(self.document())
        self.cursorPositionChanged.connect(self.matchParentheses)

    def matchParentheses(self):
        self.setExtraSelections([])
        block = self.textCursor().block()
        data = block.userData()
        if data is not None:
            abspos = self.textCursor().position()
            pos = block.position()

            for i, info in enumerate(data.parentheses):
                curpos = abspos - pos
                if info.position == curpos - 1 and info.character == "(":
                    if self.matchLeftPar(block, i+1):
                        self.createParSelection(pos + info.position)
                    else:
                        self.highlightIncomplete(pos + info.position)
                if info.position == curpos - 1 and info.character == ")":
                    if self.matchRightPar(block, i):
                        self.createParSelection(pos + info.position)
                    else:
                        self.highlightIncomplete(pos + info.position)

            for i, info in enumerate(data.brackets):
                curpos = abspos - pos
                if info.position == curpos - 1 and info.character == "[":
                    if self.matchLeftParBracket(block, i + 1):
                        self.createParSelection(pos + info.position)
                    else:
                        self.highlightIncomplete(pos + info.position)
                if info.position == curpos - 1 and info.character == "]":
                    if self.matchRightParBracket(block, i):
                        self.createParSelection(pos + info.position)
                    else:
                        self.highlightIncomplete(pos + info.position)

    def matchLeftPar(self, block, index, count=0):
        pos = block.position()
        data = block.userData()
        for i, info in enumerate(data.parentheses[index:]):
            if info.character == "(":
                count += 1
            elif info.character == ")":
                if count == 0:
                    self.createParSelection(pos + info.position)
                    return True
                else:
                    count -= 1
        block = block.next()
        if block.isValid():
            return self.matchLeftPar(block, 0, count)
        else:
            return False

    def matchRightPar(self, block, index, count=0):
        pos = block.position()
        data = block.userData()
        for i, info in enumerate(reversed(data.parentheses[:index])):
            if info.character == ")":
                count += 1
            elif info.character == "(":
                if count == 0:
                    self.createParSelection(pos + info.position)
                    return True
                else:
                    count -= 1
        block = block.previous()
        if block.isValid():
            return self.matchRightPar(block, None, count)
        else:
            self.highlightIncomplete(self.textCursor().position())
            return False

    def matchLeftParBracket(self, block, index, count=0):
        pos = block.position()
        data = block.userData()
        for i, info in enumerate(data.brackets[index:]):
            if info.character == "[":
                count += 1
            elif info.character == "]":
                if count == 0:
                    self.createParSelection(pos + info.position)
                    return True
                else:
                    count -= 1
        block = block.next()
        if block.isValid():
            return self.matchLeftParBracket(block, 0, count)
        else:
            return False

    def matchRightParBracket(self, block, index, count=0):
        pos = block.position()
        data = block.userData()
        for i, info in enumerate(reversed(data.brackets[:index])):
            if info.character == "]":
                count += 1
            elif info.character == "[":
                if count == 0:
                    self.createParSelection(pos + info.position)
                    return True
                else:
                    count -= 1
        block = block.previous()
        if block.isValid():
            return self.matchRightParBracket(block, None, count)
        else:
            self.highlightIncomplete(self.textCursor().position())
            return False

    def highlightIncomplete(self, pos):
        selection = QTextEdit.ExtraSelection()
        selection.format.setForeground(Qt.magenta)
        cursor = self.textCursor()
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
        selection.cursor = cursor
        self.setExtraSelections(self.extraSelections() + [selection])

    def createParSelection(self, pos):
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(Qt.green)
        selection.format.setForeground(Qt.black)
        cursor = self.textCursor()
        cursor.setPosition(pos)
        cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
        selection.cursor = cursor
        self.setExtraSelections(self.extraSelections() + [selection])