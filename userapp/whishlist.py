from django.conf import settings




class Whishlist(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            # save an empty wishlist in the session
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def add(self, product, quantity=1, action=None):
        """
        Add a product to the wishlist or update its quantity.
        """
        id = product.id
        newItem = True
        if str(product.id) not in self.wishlist.keys():

            self.wishlist[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'name': product.pro_name,
                'quantity': 1,
                'price': str(product.price),
                'image': product.main_image.url
            }
        else:
            newItem = True

            for key, value in self.wishlist.items():
                if key == str(product.id):

                    value['quantity'] = value['quantity'] + 1
                    newItem = False
                    self.save()
                    break
            if newItem == True:

                self.wishlist[product.id] = {
                    'userid': self.request,
                    'product_id': product.id,
                    'name': product.name,
                    'quantity': 1,
                    'price': str(product.price),
                    'image': product.image.url
                }

        self.save()

    def save(self):
        # update the session wishlist
        self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the wishlist.
        """
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()