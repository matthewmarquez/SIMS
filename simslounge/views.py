from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Lounge, LoungeMember, Resident, Proposal
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Helper Functions

def check_lounge_membership(user, lounge_id):
    # Returns whether a user in a lounge and the appropriate lounge membership
    in_lounge = False
    desired_lounge_membership = None
    for lounge_membership in user.resident.memberships.all():
        lounge = lounge_membership.lounge
        if (lounge.id == lounge_id):
            in_lounge = True
            desired_lounge_membership = lounge_membership
            break
    return (in_lounge, desired_lounge_membership)

def has_voted(membership, proposal):
    if membership in proposal.proposal_yes.all():
        return True
    elif membership in proposal.proposal_no.all():
        return True
    else:
        return False

def check_pass(proposal, lounge):
    threshold = max(len(lounge.members.all()), 5)
    if len(proposal.proposal_yes.all()) >= threshold:
        return True
    else:
        return False

def get_used_funds(lounge):
    used = 0
    for proposal in lounge.proposals.all():
        if proposal.proposal_passed:
            used += proposal.proposal_amount
    return used

def index(request):
    return HttpResponse("Hello, world.")

# Submission API

def vote(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    vote = request.POST['vote']
    if request.user.is_authenticated:
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal_lounge = proposal.proposal_lounge
        in_lounge, lounge_membership = check_lounge_membership(request.user, proposal_lounge.id)
        if in_lounge and not has_voted(request.user, proposal):
            if vote == "Yes":
                proposal.proposal_yes.add(lounge_membership)
                if check_pass(proposal, proposal_lounge):
                    proposal.proposal_passed = True
            else:
                proposal.proposal_no.add(lounge_membership)
    proposal.save()
    #update number with lounge id
    return HttpResponseRedirect(reverse('simslounge:proposals', args=(1,)))

def create_proposal(request, lounge_id):
    lounge = get_object_or_404(Lounge, pk=lounge_id)
    if request.user.is_authenticated:
        in_lounge, lounge_membership = check_lounge_membership(request.user, lounge.id)
        if in_lounge:
            name = request.POST['name']
            description = request.POST['description']
            amount = request.POST['amount']
            ilef = request.POST['ilef']
            reg_funding = True
            if ilef == "Yes":
                reg_funding = False
            new_proposal = Proposal(proposal_name=name, proposal_description=description, proposal_amount=amount, proposal_passed=False, proposal_lounge=lounge, proposal_reg_funding=reg_funding, proposal_creator=request.user.resident)
            new_proposal.save()
    return HttpResponseRedirect(reverse('simslounge:proposals', args=(1,)))

def join_lounge(request):
    pass

def create_lounge(request):
    pass


# Form API

def proposal_form(request, lounge_id):
    if request.user.is_authenticated:
        lounge = get_object_or_404(Lounge, pk=lounge_id)
        in_lounge, lounge_membership = check_lounge_membership(request.user, lounge.id)
        if in_lounge:
            return render(request, 'simslounge/newproposal.html', {'lounge': lounge})
        else:
            return HttpResponseRedirect(reverse('simslounge:mylounges'))
    else:
        return HttpResponseRedirect(reverse('simslounge:login_page'))

def vote_form(request, proposal_id):
    if request.user.is_authenticated:
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal_lounge = proposal.proposal_lounge
        in_lounge, lounge_membership = check_lounge_membership(request.user, proposal_lounge.id)
        if in_lounge and not has_voted(lounge_membership, proposal):
            return render(request, 'simslounge/vote.html', {'proposal': proposal})
        else:
            return render(request, 'simslounge/alreadyvoted.html')
    else:
        return HttpResponseRedirect(reverse('simslounge:login_page'))

def lounge_form(request):
    pass

def lounge_create_form(request):
    pass

# Standard Page API

def view_proposals(request, lounge_id):
    if request.user.is_authenticated:
        in_lounge, membership = check_lounge_membership(request.user, lounge_id)
        if in_lounge:
            lounge = get_object_or_404(Lounge, pk=lounge_id)
            proposals = lounge.proposals.all()
            used_funds = get_used_funds(lounge)
            remaining_funds = lounge.lounge_funds - used_funds
            return render(request, 'simslounge/proposals_lounge.html', {'proposals': proposals, 'lounge': lounge, 'funds_used': used_funds, 'funds_remaining': remaining_funds})
    else:
        return HttpResponseRedirect(reverse('simslounge:login_page'))

def all_proposals(request):
    proposals = Proposals.objects.all()
    return render(request, 'simslounge/proposals.html', {'proposals': proposals})

def my_lounges(request):
    if request.user.is_authenticated:
        lounge_memberships = request.user.resident.memberships
        lounges = []
        for membership in lounge_memberships.all():
            lounges.append(membership.lounge)
        return render(request, 'simslounge/mylounges.html', {'lounges': lounges, 'user': request.user})
    else:
        return HttpResponseRedirect(reverse('simslounge:login_page'))

# Authentication

def login_page(request):
    return render(request, 'simslounge/login.html')

def login_handle(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('simslounge:my_lounges'))
    else:
        return HttpResponseRedirect(reverse('simslounge:login_page'))

def logout_handle(request):
    logout(request)
    return HttpResponseRedirect(reverse('simslounge:login_page'))

