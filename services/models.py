from django.db import models
from shops.models import Shop
# AVAILABLE_SERVICES = [
#         # Man Services
#         ('HairCut_Man', 'Haircuts for men'),
#         ('BuzzCut', 'Buzz cut'),
#         ('BeardStyle', 'Beard styling'),
#         ('BeardShave', 'Beard shaving'),
#         ('NoseHair', 'Nose hair removal'),
#         # Woman Services
#         ('HairCut_Woman', 'Haircuts for women'),
#         ('HairStyle', 'Hair styling for women'),
#         ('HairMask', 'Hair masks'),
#         ('BlowDry', 'Hair blow drying'),
#         ('HairTone', 'Hair toning'),
#         ('HairBotox', 'Hair botox therapy'),
#         ('HairKeratin', 'Keratin hair straitening'),
#         # Unisex Services
#         ('HairWashing', 'Hair washing'),
#         ('ScalpMassage', 'Scalp massage'),
#         ('HairColor', 'Hair coloring'),
#         ('HairHighlight', 'Technical hair coloring'),  # шатирање и др
#     ]


class Service(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    service = models.CharField(max_length=100, default='')
    price = models.PositiveIntegerField(default=0)
    time_to_complete = models.TimeField()

    class Meta:
        unique_together = ('shop', 'service')

    def __str__(self):
        formatted_time = self.time_to_complete.strftime('%H:%M')
        return f'{self.service}\t {formatted_time} {self.price}'