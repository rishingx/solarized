#========== IMPORT ==========#

import sys
import bridge
import grid
import port

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QInputDialog, QPushButton, QLabel, QDialogButtonBox, QVBoxLayout, QMessageBox, QWidget, QTableWidget, QTableWidgetItem, QFileDialog

#========== GLOBALS ==========#

cols = {'Account Number' : 'acc', 'Name of Owner': 'name', 'Phone Number': 'ph'}
default = "./default.csv"

#========== GRAPH CLASS ==========#

class Graph(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Graph, self).__init__(fig)

#========== PANEL CLASS ==========#

class Panel(QMainWindow):
    def __init__(self):
        super(Panel, self).__init__()
        self.settings = port.load_settings()
        self.gd = grid.Grid(len(bridge.get_houses()), self.settings[0], self.settings[1], self.settings[2])
        self.revenue_hist = []

        self.setWindowTitle('Grid')
        self.layout = QVBoxLayout()

        self.setup_menus()
        self.setup_table()
        self.setup_graph()

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

#========== SETUP FUNCTIONS ==========#

    def setup_menus(self):
        self.menuBar = self.menuBar()

        #== filemenu ==#
        fileMenu = self.menuBar.addMenu('File')

        import_action = QAction('Import CSV', self)
        import_action.setShortcut('o')
        import_action.triggered.connect(lambda :self.import_csv())

        export_action = QAction('Export to CSV', self)
        export_action.setShortcut('s')
        export_action.triggered.connect(lambda :self.export_csv())
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('q')
        exit_action.triggered.connect(lambda :QApplication.quit())

        fileMenu.addAction(import_action)
        fileMenu.addAction(export_action)
        fileMenu.addAction(exit_action)
        
        #== editmenu ==#
        editMenu = self.menuBar.addMenu('Edit')

        add_action = QAction('Add House', self)
        add_action.setShortcut('a')
        add_action.triggered.connect(lambda :self.add_house())

        rem_action = QAction('Remove House', self)
        rem_action.setShortcut('v')
        rem_action.triggered.connect(lambda :self.remove_house())

        search_action = QAction('Search House', self)
        search_action.setShortcut('/')
        search_action.triggered.connect(lambda :self.search_house())

        editMenu.addAction(add_action)
        editMenu.addAction(rem_action)
        editMenu.addAction(search_action)

        #== gridmenu ==#
        gridMenu = self.menuBar.addMenu('Grid')

        cycle_action = QAction('Cycle', self)
        cycle_action.setShortcut('space')
        cycle_action.triggered.connect(lambda :self.cycle())

        ff_action = QAction('Fast Forward', self)
        ff_action.setShortcut('f')
        ff_action.triggered.connect(lambda :self.ff())

        fluc_action = QAction('Fluctuation', self)
        fluc_action.triggered.connect(lambda :self.change_fluc())

        chg_action = QAction('Power Charge', self)
        chg_action.triggered.connect(lambda :self.change_chg())

        pay_action = QAction('Power Payout', self)
        pay_action.triggered.connect(lambda :self.change_pay())

        amt_action = QAction('Get Amount', self)
        amt_action.setShortcut('g')
        amt_action.triggered.connect(lambda :self.get_amount())
        
        gridMenu.addAction(cycle_action)
        gridMenu.addAction(ff_action)
        gridMenu.addAction(fluc_action)
        gridMenu.addAction(chg_action)
        gridMenu.addAction(pay_action)
        gridMenu.addAction(amt_action)

        #== tablemenu ==#
        tableMenu = self.menuBar.addMenu('Table')

        update_action = QAction('Update', self)
        update_action.setShortcut('r')
        update_action.triggered.connect(lambda :self.update_table())

        default_action = QAction('Default Houses', self)
        default_action.setShortcut('n')
        default_action.triggered.connect(lambda :self.default_house())

        clear_action = QAction('Clear Table', self)
        clear_action.setShortcut('c')
        clear_action.triggered.connect(lambda :self.clear_house())

        tableMenu.addAction(update_action)
        tableMenu.addAction(default_action)
        tableMenu.addAction(clear_action)

        #== graphmenu ==#
        graphMenu = self.menuBar.addMenu('Graph')

        graphclr_action = QAction('Clear Graph', self)
        graphclr_action.setShortcut('x')
        graphclr_action.triggered.connect(lambda :self.clear_graph())

        graphMenu.addAction(graphclr_action)

    def setup_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Account', 'Name', 'Phone', 'Avg Prod Rate', 'Cur Prod Rate', 'Cur Cons Rate', 'Cur Diff'])
        self.table.setSortingEnabled(True)
        self.update_table()
        self.layout.addWidget(self.table)

    def setup_graph(self):
        self.sc = Graph(self, width=5, height=4, dpi=100)
        self.layout.addWidget(self.sc)
        
        self.graphbar = NavigationToolbar(self.sc)
        self.layout.addWidget(self.graphbar)
        self.draw_graph()

    def draw_graph(self):
        self.sc.axes.set_title("CONSUMPTION GRAPH")
        self.sc.axes.set_xlabel("cycles")
        self.sc.axes.set_ylabel("consumption")
        leg = self.sc.axes.legend(loc='upper right', frameon=True)
        self.sc.draw()

#========== UPDATE FUNCTIONS ==========#

    def update_table(self):
        data = bridge.get_houses()
        self.gd.houses = len(data)
        self.table.setRowCount(len(data))

        for row in range(len(data)):
            for col in range(len(data[0])):
                if type(data[row][col]) is int:
                    cell = QTableWidgetItem()
                    cell.setData(Qt.EditRole, data[row][col])
                else:
                    cell = QTableWidgetItem((data[row][col]))
                cell.setFlags(cell.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(row, col, cell)

    def update_graph(self):
        self.sc.axes.cla()
        self.sc.axes.plot(range(len(self.revenue_hist)), self.revenue_hist, color='blue', label="Consumption")
        if len(self.revenue_hist) >= 2:
            avgline = self.revenue_hist[0:1] + self.revenue_hist[-1::]
            self.sc.axes.plot([0, len(self.revenue_hist)-1], avgline, color='green', label="Average")

        zeroline = [0]*(len(self.revenue_hist))
        self.sc.axes.plot(range(len(self.revenue_hist)), zeroline, color='black', label="Zero")
        self.draw_graph()

#========== CYCLE FUNCTIONS ==========#

    def cycle(self):
        revenue = 0
        self.gd.cycle()
        self.update_table()
        data = bridge.get_houses("rate")

        for row in range(len(self.gd.cur_sheet)):
            for col in range(4,6):
                cell = QTableWidgetItem(str(data[row][0] + self.gd.cur_sheet[row][col-4]))
                self.table.setItem(row, col, cell)
            self.table.setItem(row, 6, QTableWidgetItem(str(self.gd.cur_sheet[row][2])))

        self.revenue_hist.append(round(self.gd.revenue, 4))
        self.update_graph()

    def ff(self):
        n, done1 = QInputDialog.getInt(self, 'Input Dialog', 'Enter number of cycles:', value=2, min=0)
        if done1 and self.confirm("Fast Forward", "Are you sure you want to fast forward "+str(n)+" cycles?"):
            for i in range(n):
                self.cycle()

#========== REVENUE FUNCTIONS ==========#

    def get_amount(self):
        amt = round(self.gd.get_amount(), 4)
        if amt >= 0:
            self.dialog("Revenue Generated", "A profit of "+str(amt)+" has been made.")
        else:
            self.dialog("Revenue Generated", "A loss of "+str(-amt)+" has been made.")


#========== EDIT FUNCTIONS ==========#

    def add_house(self):
        message = ""
        acc, done1 = QInputDialog.getInt(self, 'Input Dialog', 'Enter Account Number:', min=1, value=len(bridge.get_houses("acc"))+1)
        if done1:
            if (acc,) in bridge.get_houses("acc"):
                message = "Duplicate Account Number"
            else:
                name, done2 = QInputDialog.getText(self, 'Input Dialog', 'Enter Owner Name:')
                if done2 and isinstance(name, str):
                    ph, done3 = QInputDialog.getInt(self, 'Input Dialog', 'Enter Phone:', min=0)
                    if done3:
                        rate, done4 = QInputDialog.getInt(self, 'Input Dialog', 'Enter Avg Prod Rate:', min=0)
                        if done4:
                            bridge.add_house(acc, name, ph, rate)
                            message = "House Successfully Added!"
                            self.update_table()
            if message != "":
                self.dialog("Adding...", message)

    def remove_house(self):
        message = ""
        acc, done1 = QInputDialog.getInt(self, 'Input Dialog', 'Enter Account Number', min=1)
        if done1:
            if (acc,) not in bridge.get_houses("acc"):
                message = "No Such Account"
            else:
                bridge.remove_house(acc)
                message = "House Successfully Removed!"
                self.update_table()
            if message != "":
                self.dialog("Removing...", message)

    def clear_house(self):
        if self.confirm("Clear House", "Are you sure you want to clear all the houses?"):
            bridge.remove_all()
            self.update_table()

    def clear_graph(self):
        self.revenue_hist = self.revenue_hist[-1::]
        self.sc.axes.cla()
        self.draw_graph()

#========== OTHER FUNCTIONS =========#

    def search_house(self):
        global cols
        col, done1 = QInputDialog.getItem(self, 'Input Dialog', 'Choose the search category:', cols.keys())
        if done1 and col in cols.keys():
            query, done2 = QInputDialog.getText(self, 'Input Dialog', ('Enter '+col))
            if done2:
                results = bridge.search_house(cols[col], query)
                if results == []:
                    self.dialog("Search Results", "No Reuslts!")
                else:
                    dlg = QDialog()
                    dlg.setWindowTitle("Search Results")
                    buttons = QDialogButtonBox.Ok
                    dlg.buttonBox = QDialogButtonBox(buttons)
                    dlg.buttonBox.accepted.connect(dlg.accept)

                    result_table = QTableWidget()
                    result_table.setColumnCount(4)
                    result_table.setRowCount(len(results))
                    result_table.setHorizontalHeaderLabels(['Account', 'Name', 'Phone', 'Avg Prod Rate'])
                    result_table.setSortingEnabled(True)
            
                    for row in range(len(results)):
                        for col in range(len(results[0])):
                            cell = QTableWidgetItem(str(results[row][col]))
                            result_table.setItem(row, col, cell)
           
                    dlg.layout = QVBoxLayout()
                    dlg.layout.addWidget(result_table)
                    dlg.layout.addWidget(dlg.buttonBox)
                    dlg.setLayout(dlg.layout)
                    dlg.exec()

    def default_house(self):
        if self.confirm("Default House", "Do you really want to restore default houses? This will delete current data!"):
            global default
            bridge.remove_all()
            port.import_csv(default, bridge)
            self.update_table()

#========== TUNING FUNCTIONS ==========#

    def change_fluc(self):
        fluc, done = QInputDialog.getDouble(self, 'Input Dialog', 'Enter Fluctuation Level:', min=0.0, max=10.0, value=self.settings[0])
        if done:
            self.gd.fluc = fluc
            port.save_settings(fluc, self.settings[1], self.settings[2])
            self.settings = port.load_settings()
            self.dialog("Changing Fluctuation...", "Fluctuation Level Changed!")

    def change_chg(self):
        chg, done = QInputDialog.getDouble(self, 'Input Dialog', 'Enter Power Charge:', min=0.0, value=self.settings[1])
        if done:
            self.gd.chg = chg
            port.save_settings(self.settings[0], chg, self.settings[2])
            self.settings = port.load_settings()
            self.dialog("Changing Power Charge...", "Power Charge Changed!")

    def change_pay(self):
        pay, done = QInputDialog.getDouble(self, 'Input Dialog', 'Enter Power Payout:', min=0.0, value=self.settings[2])
        if done:
            self.gd.pay = pay
            port.save_settings(self.settings[0], self.settings[1], pay)
            self.settings = port.load_settings()
            self.dialog("Changing Power Payout...", "Power Payout Changed!")

#========== IMPORT-EXPORT WRAPPERS ==========#

    def import_csv(self):
        dlg, done = QFileDialog.getOpenFileUrl(self)
        if done and self.confirm("Importing...", "Are you sure you want to import from csv? Current data will be deleted!"):
            bridge.remove_all()
            port.import_csv(dlg.path(), bridge)
            self.update_table()

    def export_csv(self):
        dlg, done = QFileDialog.getSaveFileUrl(self)
        if done:
            port.export_csv(dlg.path(), bridge)

#========== UTILITY FUNCTIONS ==========#

    def dialog(self, title, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        dlg.exec()
        del dlg

    def confirm(self, title, message):
        dlg = QDialog()
        dlg.setWindowTitle(title)
        buttons = QDialogButtonBox.Yes | QDialogButtonBox.No
        dlg.buttonBox = QDialogButtonBox(buttons)
        dlg.buttonBox.accepted.connect(dlg.accept)
        dlg.buttonBox.rejected.connect(dlg.reject)

        dlg.layout = QVBoxLayout()
        dlg.layout.addWidget(QLabel(message))
        dlg.layout.addWidget(dlg.buttonBox)
        dlg.setLayout(dlg.layout)

        if dlg.exec():
            return True
        else:
            return False
        del dlg

#========== MAIN LOOP ==========#

if __name__ == '__main__':
    bridge.connect()
    bridge.create_tables()
    app = QApplication(sys.argv)
    panel = Panel()
    panel.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        bridge.disconnect()
        print("Closing Window")
