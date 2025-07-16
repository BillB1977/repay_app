from flask import Flask, render_template, request
from datetime import datetime, timedelta
from forms import PaymentForm
import math

app = Flask(__name__)
app.secret_key = 'secret_key'

FEE_30 = 50.00
FEE_50 = 100.00
BILL_DUE_DAY = 4

def calculate_plan(last_payment_date, today, rent, protection, gate, additional, late_percent):
    last_payment_date = datetime.combine(last_payment_date, datetime.min.time())
    monthly_total = rent + protection + gate + additional
    billing_dates = []
    due = datetime(last_payment_date.year, last_payment_date.month, BILL_DUE_DAY)
    if due <= last_payment_date:
        due += timedelta(days=30)
    while due <= today:
        billing_dates.append(due)
        due += timedelta(days=30)

    cycles = []
    for d in billing_dates:
        days_late = (today - d).days
        base = monthly_total
        late = 0
        if days_late >= 7:
            late += base * (late_percent / 100)
        if days_late >= 30:
            late += FEE_30
        if days_late >= 50:
            late += FEE_50
        total = round(base + late, 2)
        cycles.append({
            'due_date': d.strftime("%Y-%m-%d"),
            'base': round(base, 2),
            'late_fee': round(late, 2),
            'total': total,
            'days_late': days_late
        })

    next_due = billing_dates[-1] + timedelta(days=30)
    cycles.append({
        'due_date': next_due.strftime("%Y-%m-%d"),
        'base': round(monthly_total, 2),
        'late_fee': 0.00,
        'total': round(monthly_total, 2),
        'days_late': 0
    })

    total_due = sum(c['total'] for c in cycles)

    def generate_installments(total, duration_days):
        intervals = [0, duration_days // 2, duration_days]
        today = datetime.today()
        plan = []
        for i, offset in enumerate(intervals):
            due_date = today + timedelta(days=offset)
            plan.append({
                'installment': i + 1,
                'due_date': due_date.strftime("%Y-%m-%d"),
                'amount': round(total / len(intervals), 2)
            })
        return plan

    plans = {
        '60_day': generate_installments(total_due, 60),
        '45_day': generate_installments(total_due, 45),
        '30_day': generate_installments(total_due, 30)
    }

    return cycles, plans, round(total_due, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PaymentForm()
    if form.validate_on_submit():
        last_payment = form.last_payment.data
        rent = float(form.rent.data)
        protection = float(form.protection.data)
        gate = float(form.gate.data)
        additional = float(form.additional_costs.data)
        late_fee_percent = float(form.late_fee_percent.data)

        today = datetime.today()
        cycles, plans, total = calculate_plan(
            last_payment, today, rent, protection, gate, additional, late_fee_percent
        )
        return render_template('results.html', cycles=cycles, plans=plans, total=total)

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)