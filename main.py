from gui import MainDashboard  # Import the MainDashboard class
from database import create_tables

if __name__ == "__main__":
    # Initialize the database tables
    create_tables()

    # Start the application with the MainDashboard
    main_dashboard = MainDashboard()
    main_dashboard.mainloop()