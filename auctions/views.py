from typing import List
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import CommentForm, ListingForm
from .models import Bid, Category, Comment, Listing, User, Watchlist


def index(request):
    listings = Listing.objects.filter(active=True).order_by('-timestamp')
    paginator = Paginator(listings, 9)
    page_number = request.GET.get('page')
    active_listings = paginator.get_page(page_number)
    return render(request, 'auctions/index.html', {
        'active_listings': active_listings,
        'categories': Category.objects.order_by('name')
    })


def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories': Category.objects.order_by('name')
    })

def categories_filter(request, category_id):
    return render(request, 'auctions/index.html', {
        'active_listings': Listing.objects.filter(active=True, category=category_id).all(),
        'category': Category.objects.get(pk=category_id),
        'categories': Category.objects.order_by('name')
    })

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            title = request.POST['title']
            category = Category.objects.get(pk=int(request.POST['category']))
            description = request.POST['description']
            starting_price = request.POST['starting_price']
            picture = request.POST['picture']
            Listing.objects.create(title=title, category=category, description=description, starting_price=starting_price, picture=picture, creator=request.user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/create_listing.html', {
                'form': form
            })
    else:
        form = ListingForm()
        return render(request, 'auctions/create_listing.html', {
            'form': form,
            'categories': Category.objects.order_by('name')
        })


def show_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user.is_authenticated:
        return render(request, 'auctions/show_listing.html', {
            'listing': listing,
            'in_watchlist': Watchlist.objects.filter(user=request.user, item=Listing.objects.get(pk=int(listing_id))).exists(),
            'comments': Comment.objects.filter(listing_id=listing_id).order_by('-timestamp'),
            'form': CommentForm(),
            'categories': Category.objects.order_by('name')
        })
    else:
        return render(request, 'auctions/show_listing.html', {
        'listing': listing,
        'comments': Comment.objects.filter(listing_id=listing_id).order_by('-timestamp'),
        'form': CommentForm(),
        'categories': Category.objects.order_by('name')
    })


@login_required
def close_auction(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        messages.error(request, 'It seems that you tried to close an auction that does not exist!')
        return HttpResponseRedirect(reverse('index'))
    if request.user.id != listing.creator_id:
        return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
    else:
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse('index'))


@login_required
def place_bid(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        messages.error(request, 'You cannot place a bid on a non-existant auction!')
        return HttpResponseRedirect(reverse('index'))
    if listing.active:
        new_bid = int(request.POST['bid'])
        try:
            latest_bid = Bid.objects.filter(listing=listing).latest('timestamp')
        except Bid.DoesNotExist:
            if listing.starting_price >= new_bid:
                messages.error(request, 'Bid\'s value must be higher than the starting price of the auction.')
                return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
            else:
                Bid.objects.create(listing=listing, user=request.user, value=new_bid)
                messages.success(request, 'Your bid has been successfully placed!')
                return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
        if latest_bid is not None:
            if latest_bid.value >= new_bid:
                messages.error(request, 'Bid\'s value must be higher than the latest bid.')
                return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
            else:
                Bid.objects.create(listing=listing, user=request.user, value=new_bid)
                messages.success(request, 'Your bid has been successfully placed!')
                return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
                
    messages.error(request, 'Cannot place a bid when the auction is no longer active!')
    return HttpResponseRedirect(reverse('index'))


@login_required
def add_to_watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        messages.error(request, 'You cannot add to your watchlist an auction that does not exist!')
        return HttpResponseRedirect(reverse('index'))
    Watchlist.objects.create(user=request.user, item=listing)
    messages.success(request, 'Successfully added to your watchlist!')
    return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))


@login_required
def del_from_watchlist(request, listing_id):
    try:
        auction_in_watchlist = Watchlist.objects.filter(user=request.user, item=get_object_or_404(Listing, pk=listing_id))
    except Watchlist.DoesNotExist:
        messages.error(request, 'It seems this auction isn\'t part of your watchlist!')
        HttpResponseRedirect(reverse('watchlist'))
    auction_in_watchlist.delete()
    messages.success(request, 'Auction successfully deleted from your watchlist!')
    return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))


@login_required
def watchlist(request):
    return render(request, 'auctions/watchlist.html', {
        'watchlist': Watchlist.objects.filter(user=request.user).order_by('-item__timestamp'),
        'categories': Category.objects.order_by('name')
    })


@login_required
def post_comment(request, listing_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            listing = get_object_or_404(Listing, pk=listing_id)
            Comment.objects.create(listing=listing, user=request.user, content=request.POST['content'])
            messages.success(request, 'Comment successfully posted!')
        return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
    


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'auctions/login.html', {'categories': Category.objects.order_by('name')})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'auctions/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'auctions/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/register.html', {'categories': Category.objects.order_by('name')})
