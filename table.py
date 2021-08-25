# table builder
# july 20th 2021
# oscar yu

class table:
    def __init__(self, rows: list) -> None:
        self.rows = rows
        self.cols = [[str(row[i]) for row in rows] for i in range(len(rows[0]))]

        self.columnWidth = [len(max(column, key = len)) + 2 for column in self.cols]

    def getRows(self) -> list:
        return self.rows

    def getCols(self) -> list:
        return self.cols

    def getWidths(self) -> list:
        return self.columnWidth

    def __str__(self) -> str:
        # top format row
        output = "┌"
        for i in range(len(self.columnWidth)):
            output += "─" * self.columnWidth[i]
            if i != (len(self.columnWidth) - 1):
                output += "┬"
        output += "┐\n"

        # middle format row
        midline = "├"
        for i in range(len(self.columnWidth)):
            midline += "─" * self.columnWidth[i]
            if i != (len(self.columnWidth) - 1):
                midline += "┼"
        midline += "┤\n"

        # each line
        for i in range(len(self.rows)):
            row = self.rows[i]
            output += "|"
            for j in range(len(self.cols)):
                output += " " + str(row[j]) + " " * (self.columnWidth[j] - 1 - len(str(row[j]))) + "|"
            output += "\n"

            if i != len(self.rows) - 1:
                    output += midline
        
        # final format row
        output += "└"
        for i in range(len(self.columnWidth)):
            output += "─" * self.columnWidth[i]
            if i != (len(self.columnWidth) - 1):
                output += "┴"
        output += "┘"

        return output