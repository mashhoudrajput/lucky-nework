# ISP Payment Recovery Management System

Web-based application for managing internet service provider customer payments and recovery tracking.

## Features

- Customer Management: Add, edit, delete customers
- Payment Tracking: Track payment status (Paid/Unpaid)
- Monthly Recovery Workflow: Generate lists, update payments, track remaining
- Bulk Operations: Select multiple customers and mark as paid/unpaid
- CSV Import/Export: Import customers from CSV, export for printing
- Responsive Design: Works on mobile and desktop
- Login Authentication: Secure access with username and password

## Login Credentials

- Username: `admin` | Password: `admin@1122`
- Username: `shafeeq` | Password: `0789`

## Requirements

- Python 3.7 or higher

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:
   ```bash
   python app.py
   ```

3. Access at: http://localhost:5000

## Using Docker

1. Build the image:
   ```bash
   docker build -t isp-recovery .
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 -v $(pwd)/data:/app/data -e DATABASE_PATH=/app/data/isp_recovery.db isp-recovery
   ```

3. Access at: http://localhost:5000

## Usage

### Adding Customers
- Go to Customers page
- Click "Add Customer"
- Fill required fields: Name, Package, Payment Amount
- Phone and Address are optional

### Monthly Recovery
1. Start of Month: Go to Recovery page, export/print all customers
2. During Recovery: Mark customers as Paid as you collect payments
3. Next Day: View unpaid customers list to see remaining

### Bulk Operations
- Select multiple customers using checkboxes
- Use bulk actions to mark as paid/unpaid or delete

### Import/Export
- Import: Click "Import CSV" to add customers from CSV file
- Export: Click "Export CSV" to download customer list

## Database

- Database file: `isp_recovery.db` (created automatically)
- Location: Same folder as `app.py` (or `/app/data` in Docker)
- Backup: Regularly backup the database file

## Access from Mobile

1. Find your computer's IP address: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Access from mobile: `http://YOUR_IP:5000`
3. Ensure firewall allows port 5000
