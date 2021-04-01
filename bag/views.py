from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from products.models import Product 

def view_bag(request):
    '''
    A view that renders the bag contents page
    '''
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    '''
    Add a quantity of the specified product to the shopping bag.
    '''

    product = Product.objects.get(pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    
    bag = request.session.get('bag', {})
    print(f'Bag: {bag}')

    # If the item has a size
    if size: 
        # If the item is already in the bag / the 'keys' are the product id numbers.
        if item_id in list(bag.keys()):
            # If the size added is already listed for that item_id in the bag i.e. if there is already an item of that size in the bag.
            if size in bag[item_id]['items_by_size'].keys():
                # Add the quantity to the quantity of items of that size already in the bag. 
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # If the item is already in the bag but NOT in that size - add it in with the current quantity.
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # If the item is NOT already in the bag - add it in with the dict format below:
            bag[item_id] = {'items_by_size': { size: quantity }}
    else:
        # If the item added does NOT have sizes 
        if item_id in list(bag.keys()):
            # If the item is already in the bag, then just add to the quantity
            bag[item_id] += quantity
        else:
            # Just add it in by id and add the quantity
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag.')
    
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    '''
    Adjust the quantity of the specified product to the specified amount.
    '''

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # If the item has a size
    if size: 
        # If the adjusted quantity is more than 0 i.e. if the item has not been deleted.
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            # If quantity is set to 0 then delete that item in that size.
            del bag[item_id]['items_by_size'][size]
            # If there are none of the same item in other sizes then just remove the item_id (item) completely.
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        # If the item doesn't have a size and the quantity is set to greater than 0
        if quantity > 0:
            # set the quantity to the quantity
            bag[item_id] = quantity
        else:
            # If the quantity is set to 0 - then pop the item.
            bag.pop(item_id)
    
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    '''
    Adjust the quantity of the specified product to the specified amount.
    '''
    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        # If the item has a size
        if size: 
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            else:
                # If quantity is set to 0 then delete that item in that size.
                del bag[item_id]['items_by_size'][size]
        else:
            bag.pop(item_id)
        
        request.session['bag'] = bag
        return HttpResponse(status=200)
    
    except Exception as e:
        return HttpResponse(status=500)