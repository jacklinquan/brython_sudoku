from browser import document, html, window, alert, console, bind  # type: ignore
import random

from sudoku_solver import SudokuBoard, SudokuSolver
from sudoku_generator import SudokuGenerator


def main():
    # Header
    document <= html.NAV(
        html.DIV(
            html.DIV("Sudoku", Class="brand-logo center"),
            Class="nav-wrapper container center",
        ),
        Class="teal",
        role="navigation",
    )

    # Leave some space
    document <= html.P()

    rbs_levels = html.FORM(action="#")
    rb_beginner = html.INPUT(name="group1", type="radio", checked=True)
    rb_easy = html.INPUT(name="group1", type="radio")
    rb_medium = html.INPUT(name="group1", type="radio")
    rb_hard = html.INPUT(name="group1", type="radio")
    rb_expert = html.INPUT(name="group1", type="radio")

    rbs_levels <= html.LABEL(rb_beginner) <= html.SPAN("Beginner", Class="col s4 m2")
    rbs_levels <= html.LABEL(rb_easy) <= html.SPAN("Easy", Class="col s4 m2")
    rbs_levels <= html.LABEL(rb_medium) <= html.SPAN("Medium", Class="col s4 m2")
    rbs_levels <= html.LABEL(rb_hard) <= html.SPAN("Hard", Class="col s4 m2")
    rbs_levels <= html.LABEL(rb_expert) <= html.SPAN("Expert", Class="col s4 m2")

    document <= html.P()
    document <= html.DIV(Class="row") <= html.DIV(Class="container") <= rbs_levels

    def generate_puzzle(ev):
        nonlocal generated_sdm
        puzzle.clear()
        alert("It could take some time to generate a new puzzle.")
        if rb_beginner.checked:
            level = 46
        elif rb_easy.checked:
            level = 40
        elif rb_medium.checked:
            level = 34
        elif rb_hard.checked:
            level = 28
        elif rb_expert.checked:
            level = 17
        else:
            level = 46
        generated_sdm = SudokuGenerator().generate_level(level=level).get_sdm()
        puzzle <= make_grid(generated_sdm)
        btn_generate.disabled = True

    btn_generate = html.BUTTON(
        "Generate", Class="btn waves-effect waves-light", disabled=True
    )
    btn_generate.bind("click", generate_puzzle)
    document <= html.DIV(Class="row") <= html.DIV(Class="container") <= btn_generate

    current_cell = None

    def entry_keypress(ev):
        ev.preventDefault()
        ev.stopPropagation()
        target = ev.target
        is_digit = ev.key.isdigit()
        if is_digit:
            value = ev.key
            cell = ev.target.parent
            cell.clear()
            cell.text = value

            sdm = "".join(
                cell.text or " " for cell in puzzle.get(selector="TD")
            ).replace(" ", "0")
            print(sdm)
            if SudokuBoard(sdm).is_solved():
                solve(None)
                alert("The puzzle is solved.")

            # jump to next cell
            # cell_rank = int(cell.id[1:])
            # if cell_rank < 80:
            #     next_cell = puzzle.get(selector="TD")[cell_rank + 1]
            #     make_input(next_cell)

    def entry_keydown(ev):
        is_tab = ev.key == "Tab"
        if is_tab:
            ev.preventDefault()
            ev.stopPropagation()
            value = ev.target.value
            cell = ev.target.parent
            cell.clear()
            cell.text = value

            # jump to next cell
            cell_rank = int(cell.id[1:])
            if not ev.shiftKey:
                if cell_rank < 80:
                    next_cell = puzzle.get(selector="TD")[cell_rank + 1]
                    make_input(next_cell)
            else:  # shift tab
                if cell_rank > 0:
                    next_cell = puzzle.get(selector="TD")[cell_rank - 1]
                    make_input(next_cell)

    def end_entry(ev):
        nonlocal current_cell
        if current_cell is not None:
            inputs = current_cell.get(selector="INPUT")
            if inputs:
                value = inputs[0].value
                current_cell.clear()
                current_cell.text = value

    def entry(ev):
        end_entry(ev)
        make_input(ev.target)

    def entry_blur(ev):
        end_entry(ev)

    def make_input(cell):
        nonlocal current_cell
        value = cell.text.strip()
        cell.clear()
        input = html.INPUT(value=value, style={"width": "1.3em", "padding": "0px"})
        cell <= input
        # input.bind("keydown", entry_keydown)
        input.bind("keypress", entry_keypress)
        input.focus()
        input.select()
        current_cell = cell

    def make_grid(grid):
        # returns an HTML table with 9 rows and 9 columns
        nonlocal current_cell

        t = html.TABLE()
        for i in range(3):
            cg = html.COLGROUP()
            for j in range(3):
                cg <= html.COL()
            t <= cg
        srow = -1
        for i, val in enumerate(grid):
            row, column = divmod(i, 9)
            if row > srow:
                if row % 3 == 0:
                    tb = html.TBODY()
                    t <= tb
                line = html.TR()
                tb <= line
                srow = row
            if val == "0":
                val = " "
                cell = html.TD(val, id="i%s" % i)
                cell.bind("click", entry)
                cell.style.contentEditable = True
            else:
                cell = html.TD(val, id="i%s" % i, Class="grey lighten-2")
                cell.style.contentEditable = False
            if column % 3 == 0:
                cell.style.borderLeftWidth = "1px"
            if column == 8:
                cell.style.borderRightWidth = "1px"
            line <= cell

        current_cell = None
        return t

    puzzle = html.SPAN(Class="left")
    # generated_sdm = SudokuGenerator().generate_level(level=SudokuGenerator.BEGINNER).get_sdm()
    generated_sdm = random.choice(
        [
            "001980600406020810582640037200009703319070008860230091020150376100460250653702100",
            "568004090310589206094000051739152000481076020652948700845001002106803075003020008",
            "140608309930140002080203040000060914201700506564981270716050028420800735300420000",
            "005601042700090000321000000819046230000300500053917684108704309097283416030169875",
            "000149250046250900502076041025030607067890005800700302680500739203980064079000028",
            "009000346804203790631040285213680900080700403900135608000090102470012500100506034",
            "683105097014780062027003500001950603000310045360874210200067030478230050130590004",
            "145008206086024503020756100007240651562001700419507300090600005671095000354010960",
            "600280309803706020007030840578492630030070052426500790980350004702804903300009587",
            "901420067000000203087063501000600904863509070000231085128794356079352018300186020",
            "100040683048500709607013020060090050479251036010786002930170268200630470750020301",
            "080051096901700280265480107009864702412903560800020000627310900098542603300090020",
            "539102876048065120260837000092006438380200960076309250620490000000020004004070382",
            "709563402803724510520000736205970800070402903000306027080005370001240690697030005",
            "753008600086190527009007480372049100890016200600302090567901042038670051040085306",
            "205876104014052087900043005700310950003504760102090040401239070500781030007465019",
            "049000106028060470050700809064325900007890564905006310502683701073910000010547290",
            "008605014471200060609140230584003020000050349903064001840500173015380092092001080",
            "173045860590008741800097000420800657015076980600050403004031598900004100051600230",
            "781204506000038197903016200208607010000321869000980002000009708017402953540870621",
        ]
    )
    puzzle <= make_grid(generated_sdm)
    document <= html.P()
    document <= html.DIV(Class="row") <= html.DIV(Class="container") <= puzzle

    def solve(ev):
        solution_board = SudokuSolver().get_1_solution(SudokuBoard(generated_sdm))
        puzzle.clear()
        puzzle <= make_grid(solution_board.get_sdm())
        btn_generate.disabled = False

    btn_solve = html.BUTTON("Solve", Class="btn waves-effect waves-light")
    btn_solve.bind("click", solve)
    document <= html.DIV(Class="row") <= html.DIV(Class="container") <= btn_solve

    # Must do window.M.AutoInit() after all html being loaded!
    window.M.AutoInit()


if __name__ == "__main__":
    main()
