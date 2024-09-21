"""
Farm Management System
A GUI application to manage crop records using PyQt5 and SQLite.
"""

import sys
import sqlite3

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QMessageBox)


# Database setup
try:
    conn = sqlite3.connect('farm_management.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS CropRecords (
        RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
        CropName TEXT,
        PlantingDate TEXT,
        HarvestDate TEXT,
        Yield REAL,
        FixedCost REAL,
        VariableCost REAL,
        Revenue REAL,
        Profit REAL
    )
    ''')

    conn.commit()
except sqlite3.Error as db_error:
    print(f"Error connecting to database: {db_error}")
    sys.exit(1)

class FarmApp(QWidget):
    """
    FarmApp class to create the main application window.
    """

    def __init__(self):
        """
        Initialize the application window and its components.
        """
        super().__init__()
        self.init_ui()
        self.current_record_id = None

    def init_ui(self):
        """
        Set up the user interface components.
        """
        self.setWindowTitle('Farm Management System')

        # Labels and Entries
        self.crop_name_label = QLabel('Crop Name')
        self.crop_name_entry = QLineEdit()

        self.planting_date_label = QLabel('Planting Date')
        self.planting_date_entry = QLineEdit()

        self.harvest_date_label = QLabel('Harvest Date')
        self.harvest_date_entry = QLineEdit()

        self.yield_label = QLabel('Yield')
        self.yield_entry = QLineEdit()

        self.fixed_cost_label = QLabel('Fixed Cost')
        self.fixed_cost_entry = QLineEdit()

        self.variable_cost_label = QLabel('Variable Cost')
        self.variable_cost_entry = QLineEdit()

        self.revenue_label = QLabel('Revenue')
        self.revenue_entry = QLineEdit()

        self.profit_label = QLabel('Profit')
        self.profit_entry = QLineEdit()

        # Buttons
        self.add_button = QPushButton('Add Record')
        self.add_button.clicked.connect(self.add_record)

        self.next_button = QPushButton('Next Record')
        self.next_button.clicked.connect(self.next_record)

        self.prev_button = QPushButton('Previous Record')
        self.prev_button.clicked.connect(self.prev_record)

        self.delete_button = QPushButton('Delete Record')
        self.delete_button.clicked.connect(self.delete_record)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.crop_name_label)
        layout.addWidget(self.crop_name_entry)
        layout.addWidget(self.planting_date_label)
        layout.addWidget(self.planting_date_entry)
        layout.addWidget(self.harvest_date_label)
        layout.addWidget(self.harvest_date_entry)
        layout.addWidget(self.yield_label)
        layout.addWidget(self.yield_entry)
        layout.addWidget(self.fixed_cost_label)
        layout.addWidget(self.fixed_cost_entry)
        layout.addWidget(self.variable_cost_label)
        layout.addWidget(self.variable_cost_entry)
        layout.addWidget(self.revenue_label)
        layout.addWidget(self.revenue_entry)
        layout.addWidget(self.profit_label)
        layout.addWidget(self.profit_entry)
        layout.addWidget(self.add_button)
        layout.addWidget(self.next_button)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def add_record(self):
        """
        Add a new crop record to the database.
        """
        try:
            crop_name = self.crop_name_entry.text()
            planting_date = self.planting_date_entry.text()
            harvest_date = self.harvest_date_entry.text()
            yield_amount = self.yield_entry.text()
            fixed_cost = self.fixed_cost_entry.text()
            variable_cost = self.variable_cost_entry.text()
            revenue = self.revenue_entry.text()
            profit = self.profit_entry.text()

            c.execute('''
            INSERT INTO CropRecords (CropName, PlantingDate, HarvestDate, Yield, FixedCost, 
                                     VariableCost, Revenue, Profit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (crop_name, planting_date, harvest_date, yield_amount, fixed_cost, 
                  variable_cost, revenue, profit))

            conn.commit()
            QMessageBox.information(self, 'Success', 'Record added successfully')
        except sqlite3.Error as db_error:
            QMessageBox.critical(self, 'Database Error', f"Error adding record: {db_error}")
        except ValueError as val_error:
            QMessageBox.critical(self, 'Value Error', f"Invalid input: {val_error}")
        except Exception as general_error:
            QMessageBox.critical(self, 'Error', f"An unexpected error occurred: {general_error}")

    def load_record(self, record):
        """
        Load a record into the input fields.
        """
        self.current_record_id = record[0]
        self.crop_name_entry.setText(record[1])
        self.planting_date_entry.setText(record[2])
        self.harvest_date_entry.setText(record[3])
        self.yield_entry.setText(str(record[4]))
        self.fixed_cost_entry.setText(str(record[5]))
        self.variable_cost_entry.setText(str(record[6]))
        self.revenue_entry.setText(str(record[7]))
        self.profit_entry.setText(str(record[8]))

    def next_record(self):
        """
        Load the next record from the database.
        """
        try:
            if self.current_record_id is None:
                c.execute('SELECT * FROM CropRecords ORDER BY RecordID ASC LIMIT 1')
            else:
                c.execute('SELECT * FROM CropRecords WHERE RecordID > ? ORDER BY RecordID ASC LIMIT 1', 
                          (self.current_record_id,))
            record = c.fetchone()
            if record:
                self.load_record(record)
            else:
                QMessageBox.information(self, 'Info', 'No more records.')
        except sqlite3.Error as db_error:
            QMessageBox.critical(self, 'Database Error', f"Error fetching record: {db_error}")

    def prev_record(self):
        """
        Load the previous record from the database.
        """
        try:
            if self.current_record_id is None:
                c.execute('SELECT * FROM CropRecords ORDER BY RecordID DESC LIMIT 1')
            else:
                c.execute('SELECT * FROM CropRecords WHERE RecordID < ? ORDER BY RecordID DESC LIMIT 1', 
                          (self.current_record_id,))
            record = c.fetchone()
            if record:
                self.load_record(record)
            else:
                QMessageBox.information(self, 'Info', 'No more records.')
        except sqlite3.Error as db_error:
            QMessageBox.critical(self, 'Database Error', f"Error fetching record: {db_error}")

    def delete_record(self):
        """
        Delete the current record from the database.
        """
        try:
            if self.current_record_id is None:
                QMessageBox.warning(self, 'Warning', 'No record selected to delete.')
                return

            c.execute('DELETE FROM CropRecords WHERE RecordID = ?', (self.current_record_id,))
            conn.commit()
            QMessageBox.information(self, 'Success', 'Record deleted successfully')
            self.clear_fields()
            self.current_record_id = None
        except sqlite3.Error as db_error:
            QMessageBox.critical(self, 'Database Error', f"Error deleting record: {db_error}")

    def clear_fields(self):
        """
        Clear the input fields.
        """
        self.crop_name_entry.clear()
        self.planting_date_entry.clear()
        self.harvest_date_entry.clear()
        self.yield_entry.clear()
        self.fixed_cost_entry.clear()
        self.variable_cost_entry.clear()
        self.revenue_entry.clear()
        self.profit_entry.clear()

# Run the application
def main():
    """
    Main function to run the application.
    """
    try:
        app = QApplication(sys.argv)
        ex = FarmApp()
        ex.show()
        sys.exit(app.exec_())
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")
        sys.exit(1)

if __name__ == '__main__':
    main()

# Close the database connection when the application is closed
try:
    conn.close()
except sqlite3.Error as db_error:
    print(f"Error closing the database connection: {db_error}")
