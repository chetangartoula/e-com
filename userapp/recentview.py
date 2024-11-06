
from django.conf import settings
from django.shortcuts import redirect

class RecentView(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        recent_view_product = self.session.get(settings.RECENT_VIEW_SESSION_ID)
        if not recent_view_product:
            # save an empty recent_view_product in the session
            recent_view_product = self.session[settings.RECENT_VIEW_SESSION_ID] = {}
            
        self.recent_view_product = recent_view_product

    def add(self, product, action=None):
        """
        Add a product to the recent_view_product or update its quantity.
        """
        id = product.id
        newItem = True
        if str(product.id) not in self.recent_view_product.keys():

            self.recent_view_product[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
               
            }
        else:
            newItem = True

            for key, value in self.recent_view_product.items():
                if key == str(product.id):

                   
                    newItem = False
                    self.save()
                    break
            if newItem == True:

                self.recent_view_product[product.id] = {
                    'userid': self.request,
                    'product_id': product.id,
                   
                }

        self.save()

    def save(self):
        # update the session recent_view_product
        self.session[settings.RECENT_VIEW_SESSION_ID] = self.recent_view_product
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True