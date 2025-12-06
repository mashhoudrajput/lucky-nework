from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, flash, session
from functools import wraps
from database import (
    init_db, add_customer, get_all_customers, get_customer_by_id,
    update_customer, delete_customer, update_payment_status,
    get_customers_by_status, get_statistics, bulk_update_payment_status,
    bulk_delete_customers
)
import csv
import io
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'lucky-network-secret-key-change-in-production'

USERS = {
    'admin': generate_password_hash('admin@1122'),
    'shafeeq': generate_password_hash('0789')
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if username in USERS and check_password_hash(USERS[username], password):
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    if 'user' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    stats = get_statistics()
    return render_template('index.html', stats=stats, username=session.get('user'))

@app.route('/customers')
@login_required
def customers():
    status_filter = request.args.get('status', 'All')
    customers = get_customers_by_status(status_filter)
    stats = get_statistics()
    return render_template('customers.html', customers=customers, current_filter=status_filter, stats=stats)

@app.route('/recovery')
@login_required
def recovery():
    status_filter = request.args.get('status', 'Unpaid')
    customers = get_customers_by_status(status_filter)
    stats = get_statistics()
    return render_template('recovery.html', customers=customers, current_filter=status_filter, stats=stats)

@app.route('/api/customer', methods=['POST'])
@login_required
def create_customer():
    try:
        data = request.json
        
        if not data.get('name') or not data.get('name').strip():
            return jsonify({'success': False, 'error': 'Name is required'}), 400
        if not data.get('package') or not data.get('package').strip():
            return jsonify({'success': False, 'error': 'Package is required'}), 400
        if not data.get('payment_amount'):
            return jsonify({'success': False, 'error': 'Monthly Payment Amount is required'}), 400
        
        customer_id = add_customer(
            data['name'].strip(),
            data.get('phone', '').strip() or 'N/A',
            data.get('address', '').strip() or 'N/A',
            data['package'].strip(),
            float(data['payment_amount'])
        )
        return jsonify({'success': True, 'id': customer_id}), 201
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid payment amount'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/customer/<int:customer_id>', methods=['PUT'])
@login_required
def update_customer_api(customer_id):
    try:
        data = request.json
        
        if not data.get('name') or not data.get('name').strip():
            return jsonify({'success': False, 'error': 'Name is required'}), 400
        if not data.get('package') or not data.get('package').strip():
            return jsonify({'success': False, 'error': 'Package is required'}), 400
        if not data.get('payment_amount'):
            return jsonify({'success': False, 'error': 'Monthly Payment Amount is required'}), 400
        
        update_customer(
            customer_id,
            data['name'].strip(),
            data.get('phone', '').strip() or 'N/A',
            data.get('address', '').strip() or 'N/A',
            data['package'].strip(),
            float(data['payment_amount'])
        )
        return jsonify({'success': True}), 200
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid payment amount'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/customer/<int:customer_id>', methods=['DELETE'])
@login_required
def delete_customer_api(customer_id):
    try:
        delete_customer(customer_id)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/customer/<int:customer_id>/payment', methods=['PUT'])
@login_required
def update_payment(customer_id):
    try:
        data = request.json
        update_payment_status(customer_id, data['payment_status'])
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/customers/bulk-payment', methods=['PUT'])
@login_required
def bulk_update_payment():
    try:
        data = request.json
        customer_ids = [int(id) for id in data.get('customer_ids', [])]
        payment_status = data.get('payment_status', 'Paid')
        
        if not customer_ids:
            return jsonify({'success': False, 'error': 'No customers selected'}), 400
        
        count = bulk_update_payment_status(customer_ids, payment_status)
        return jsonify({'success': True, 'count': count}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/customers/bulk-delete', methods=['DELETE'])
@login_required
def bulk_delete():
    try:
        data = request.json
        customer_ids = [int(id) for id in data.get('customer_ids', [])]
        
        if not customer_ids:
            return jsonify({'success': False, 'error': 'No customers selected'}), 400
        
        count = bulk_delete_customers(customer_ids)
        return jsonify({'success': True, 'count': count}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/export/customers')
@login_required
def export_customers():
    status_filter = request.args.get('status', 'All')
    customers = get_customers_by_status(status_filter)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Name', 'Phone', 'Address', 'Package', 'Payment Amount (Rs.)', 'Payment Status', 'Last Payment Date'])
    
    for customer in customers:
        writer.writerow([
            customer['id'],
            customer['name'],
            customer['phone'],
            customer['address'],
            customer['package'],
            customer['payment_amount'],
            customer['payment_status'],
            customer['last_payment_date'] or 'N/A'
        ])
    
    output.seek(0)
    filename = f"customers_{status_filter.lower()}_{datetime.now().strftime('%Y%m%d')}.csv"
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@app.route('/import/customers', methods=['POST'])
@login_required
def import_customers():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'File must be a CSV file'}), 400
        
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        imported = 0
        errors = []
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                name = row.get('Name') or row.get('name') or row.get('NAME')
                phone = row.get('Phone') or row.get('phone') or row.get('PHONE') or ''
                address = row.get('Address') or row.get('address') or row.get('ADDRESS') or ''
                package = row.get('Package') or row.get('package') or row.get('PACKAGE')
                payment = row.get('Payment Amount') or row.get('Payment Amount (Rs.)') or row.get('payment_amount') or row.get('Payment')
                
                if not name or not name.strip():
                    errors.append(f"Row {row_num}: Name is required")
                    continue
                if not package or not package.strip():
                    errors.append(f"Row {row_num}: Package is required")
                    continue
                if not payment:
                    errors.append(f"Row {row_num}: Monthly Payment Amount is required")
                    continue
                
                try:
                    payment_amount = float(str(payment).replace('₹', '').replace('Rs.', '').replace(',', '').strip())
                except ValueError:
                    errors.append(f"Row {row_num}: Invalid payment amount")
                    continue
                
                add_customer(
                    name.strip(), 
                    phone.strip() or 'N/A', 
                    address.strip() or 'N/A', 
                    package.strip(), 
                    payment_amount
                )
                imported += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
        
        return jsonify({
            'success': True,
            'imported': imported,
            'errors': errors[:10]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/statistics')
@login_required
def get_stats():
    stats = get_statistics()
    return jsonify(stats)

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    
    print("\n" + "="*50)
    print("ISP Payment Recovery System")
    print("="*50)
    print("\nServer starting...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
