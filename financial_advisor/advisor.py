# financial_advisor/advisor.py

from django.utils import timezone
from expenses.models import Expense
from userincome.models import UserIncome

def get_financial_advice_data(user):
    today = timezone.now()
    week_start = today - timezone.timedelta(days=30)

    # Fetch incomes and expenses from the past week
    incomes = UserIncome.objects.filter(owner=user, date__range=[week_start, today])
    expenses = Expense.objects.filter(owner=user, date__range=[week_start, today])

    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    savings = total_income - total_expenses
    savings_target = round(0.2 * total_income, 2) if total_income else 0

    advice = []

    # Summary with emojis
    advice.append(
        f"📊 **Monthly Summary:** 💰 Income: ₹{total_income:.2f}, 💸 Expenses: ₹{total_expenses:.2f}, 💼 Savings: ₹{savings:.2f}"
    )

    # Health tips
    if total_income == 0:
        advice.append("⚠️ No income this week — consider freelancing, part-time gigs, or upskilling!")
    elif total_expenses > total_income:
        advice.append("🚨 You're overspending! Review subscriptions, dining out, or non-essentials.")
    elif savings < 0.1 * total_income:
        advice.append(f"🪙 Try to save more! Your savings (₹{savings:.2f}) are below 10% of your income.")
    else:
        advice.append("✅ Nice work! You're saving efficiently. Stay consistent! 💪")

    # Top expense category
    category_totals = {}
    for expense in expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    top_category = max(category_totals.items(), key=lambda x: x[1], default=(None, 0))
    if top_category[0] and top_category[1] > 0.3 * total_expenses:
        advice.append(f"🔍 Major spending in **{top_category[0]}** (₹{top_category[1]:.2f}). Consider adjustments.")

    # Investment suggestions
    if savings > 0:
        advice.append(f"📈 You’ve saved ₹{savings:.2f}. Start investing to grow it!")
        advice.append("💹 Try SIPs, mutual funds, or index funds for stable returns.")
        if savings > 5000:
            advice.append("🏡 Consider long-term options: real estate, gold, ETFs.")
        advice.append("🧠 Tip: Diversify. Mix low-risk and high-growth assets!")

    # Portfolio advice
    advice.append(
        "📊 Suggested Portfolio:\n"
        "- 50% in stable (FDs, SIPs)\n"
        "- 30% in growth (stocks, mutual funds)\n"
        "- 20% in emergency fund (savings account or liquid funds)"
    )

    return {
        "income": round(total_income, 2),
        "expenses": round(total_expenses, 2),
        "savings_target": savings_target,
        "advice": advice,
    }
