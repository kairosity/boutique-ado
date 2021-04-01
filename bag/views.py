from django.shortcuts import render, redirect, get_object_or_404

def view_bag(request):
    '''
    A view that renders the bag contents page
    '''
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    '''
    Add a quantity of the specified product to the shopping bag.
    '''

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
    
    request.session['bag'] = bag
    return redirect(redirect_url)
