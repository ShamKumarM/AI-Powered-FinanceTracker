from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal
from .forms import GoalForm, AddAmountForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

@login_required(login_url='/authentication/login')
def add_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)  # Prevent immediate DB save
            goal.owner = request.user       # Assign owner before saving
            goal.save()
            messages.success(request, "Goal added successfully!")
            return redirect('list_goals')

        messages.error(request, "There was an error adding your goal. Please try again.")

    form = GoalForm()
    return render(request, 'goals/add_goals.html', {'form': form})


@login_required(login_url='/authentication/login')
def list_goals(request):
    goals = Goal.objects.filter(owner=request.user)  # Fetch only user-specific goals
    add_amount_form = AddAmountForm() 
    return render(request, 'goals/list_goals.html', {'goals': goals, 'add_amount_form': add_amount_form})


@login_required(login_url='/authentication/login')
def add_amount(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id, owner=request.user)

    if request.method == 'POST':
        form = AddAmountForm(request.POST)
        if form.is_valid():
            additional_amount = form.cleaned_data['additional_amount']
            amount_required = goal.amount_to_save - goal.current_saved_amount

            if additional_amount > amount_required:
                messages.error(request, f'The maximum amount needed to achieve goal is: {amount_required}.')
            else:
                goal.current_saved_amount += additional_amount
                goal.save()

                if goal.current_saved_amount == goal.amount_to_save:
                    # Send congratulatory email to the user
                    send_congratulatory_email(request.user.email, goal)
                    messages.success(request, 'Congratulations! You have achieved your goal.')

                    # Mark goal as achieved
                    goal.is_achieved = True
                    goal.save()

                else:
                    messages.success(request, f'Amount successfully added! Total saved amount: {goal.current_saved_amount}.')
                    messages.info(request, f'Amount still needed to reach goal: {goal.amount_to_save - goal.current_saved_amount}.')

        else:
            messages.error(request, "Invalid amount entered. Please try again.")

    return redirect('list_goals')


def send_congratulatory_email(email, goal):
    subject = 'Congratulations on achieving your goal!'
    message = f'Dear User,\n\nCongratulations on achieving your goal "{goal.name}"! You have successfully saved {goal.amount_to_save}.\n\nKeep up the good work!\n\nBest regards,\nThe Goal Tracker Team,\nExpenseWise Team'
    send_mail(subject, message, 'hemantshirsath24@gmail.com', [email])


@login_required(login_url='/authentication/login')
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, owner=request.user)
    goal.delete()
    messages.success(request, "Goal deleted successfully!")
    return redirect('list_goals')
