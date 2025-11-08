# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self.update_single_item_quality(item)

    def update_single_item_quality(self, item):
        if item.name == "Sulfuras, Hand of Ragnaros":
            return #sulfuras never changes
    
        self.decrease_sell_in(item)
    
        if item.name == "Aged Brie":
            self.update_aged_brie(item)
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            self.update_backstage_pass(item)
        else:
            self.update_normal_item(item)

    def decrease_sell_in(self, item):
        if item.name != "Sulfuras, Hand of Ragnaros":#by mistake
            item.sell_in -= 1

    def update_aged_brie(self, item):
        self.increase_quality(item)#aged brie increases in quality over time
        if item.sell_in < 0:
            self.increase_quality(item)#aged brie increases twice after expiration date

    def update_backstage_pass(self, item):
        self.increase_quality(item)#backstage passes increase in quality when concert is about to happen
    
        if item.sell_in < 10:#backstage passes increase in quality extra when concert is within 10 days
            self.increase_quality(item)
        if item.sell_in < 5:#backstage passes increase in quality a lot when concert is within 5 days
            self.increase_quality(item)
        if item.sell_in < 0:#backstage passes is useless after the concert
            item.quality = 0

    def update_normal_item(self, item):
        self.decrease_quality(item)
        if item.sell_in < 0:
            self.decrease_quality(item)

    def increase_quality(self, item):
        if item.quality < 50:#quality capped at 50
            item.quality += 1

    def decrease_quality(self, item):
        if item.quality > 0:#quality can't be below 0
            item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
