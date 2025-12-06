# ISP Payment Recovery Management System

A web-based application for managing internet service provider customer payments and recovery tracking. Designed for managing 500+ customers with monthly payment collection workflow.

## Features

- **Customer Management**: Add, edit, delete, and view customer information
- **Payment Tracking**: Track payment status (Paid/Unpaid) for each customer
- **Monthly Recovery Workflow**: 
  - Generate complete customer list at start of month
  - Update payment status as you collect payments
  - View remaining unpaid customers next day
- **Export & Print**: Export customer lists to CSV and print directly from browser
- **Responsive Design**: Works on both mobile and desktop devices
- **Local Database**: All data stored locally on your computer (SQLite)

## Requirements

- Python 3.7 or higher
- Internet connection (for Bootstrap CDN, only needed once)

## Installation & Setup

### Option 1: Cloud Server Deployment (Production)

For deploying on a cloud server (AWS, DigitalOcean, Azure, etc.), see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick start:**
```bash
git clone https://github.com/mashhoudrajput/lucky-nework.git
cd lucky-nework
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Using Docker (Local Development)

1. **Install Docker Desktop**
   - Download from https://www.docker.com/products/docker-desktop/
   - Install and start Docker Desktop

2. **Build and Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```
   This will:
   - Build the Docker image
   - Start the application on port 5000
   - Persist database data on your computer

3. **Access the Application**
   - From your computer: http://localhost:5000
   - From mobile/other devices: http://YOUR_COMPUTER_IP:5000

4. **Stop the Application**
   ```bash
   docker-compose down
   ```

5. **View Logs**
   ```bash
   docker-compose logs -f
   ```

### Option 2: Direct Python Installation

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Install Dependencies**
   - Open Command Prompt or PowerShell in this folder
   - Run: `pip install -r requirements.txt`

3. **Start the Application**
   - Run: `python app.py`
   - The application will start on http://localhost:5000

4. **Add Sample Data (Optional - for testing)**
   - In a new terminal/command prompt, run: `python add_sample_data.py`
   - This will add 20 sample customers for testing purposes
   - You can skip this step if you want to add real customers manually

## Access from Mobile/Other Devices
   - Find your computer's IP address:
     - Open Command Prompt
     - Type: `ipconfig`
     - Look for "IPv4 Address" (e.g., 192.168.1.100)
   - On your mobile/other device, open browser and go to: `http://YOUR_IP:5000`
   - **Important**: Make sure your firewall allows connections on port 5000

## Usage Guide

### Adding Customers
1. Go to "Customers" page
2. Click "Add Customer" button
3. Fill in all required fields:
   - Name
   - Phone Number
   - Address
   - Package (e.g., 50 Mbps, 100 Mbps)
   - Monthly Payment Amount
4. Click "Save Customer"

### Monthly Recovery Process

1. **Start of Month - Print Customer List**
   - Go to "Recovery" page
   - Select "All Customers" filter
   - Click "Print" button or "Export to CSV"
   - Take this list for field recovery

2. **During Recovery - Update Payments**
   - Go to "Recovery" page
   - Find the customer in the list
   - Click "Mark Paid" button when payment is collected
   - The status will update immediately

3. **Next Day - Check Remaining**
   - Go to "Recovery" page
   - Select "Unpaid" filter (or it will default to unpaid)
   - View list of customers who still need to pay
   - Export or print this list if needed
   - Continue recovery process

### Editing/Deleting Customers
- On "Customers" page, click the edit (pencil) icon to modify customer information
- Click the delete (trash) icon to remove a customer

### Exporting Data
- Go to "Recovery" or "Customers" page
- Select desired filter (All/Paid/Unpaid)
- Click "Export to CSV" button
- The file will download automatically

## Database

- Database file: `isp_recovery.db` (created automatically)
- **With Docker**: Database is persisted in the project folder (mapped volume)
- **Without Docker**: Location is same folder as `app.py`
- **Important**: Keep this file safe as it contains all your customer data
- **Backup**: Regularly backup `isp_recovery.db` file

## Troubleshooting

**Can't access from mobile device:**
- Check that both devices are on the same Wi-Fi network
- Verify your computer's IP address hasn't changed
- Make sure Windows Firewall allows port 5000
- Try disabling firewall temporarily to test
- If using Docker, check that port 5000 is properly mapped

**Application won't start:**
- Make sure Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is already in use

**Data loss:**
- Always backup the `isp_recovery.db` file regularly
- Keep copies on external drive or cloud storage

## Support

For issues or questions, check:
- Make sure all dependencies are installed correctly
- Verify Python version is 3.7 or higher
- Check that port 5000 is not blocked by firewall

## Notes

- All data is stored locally on your computer
- No internet required after initial Bootstrap loading (can work offline)
- Database file (`isp_recovery.db`) should be backed up regularly
- Application runs on your computer - keep it running when accessing from mobile

