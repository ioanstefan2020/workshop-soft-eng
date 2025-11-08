# -*- coding: utf-8 -*-
import unittest
import sys
from contextlib import redirect_stdout

from gilded_rose import Item, GildedRose
from texttest_fixture import *


class GildedRoseTest(unittest.TestCase):
    def test_normal_item_name_unchanged(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)

    def test_normal_item_quality_decreases_by_one(self):
        items = [Item("smth", 2, 100)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(99, items[0].quality)
    def test_normal_item_quality_decreases_twice_as_fast_after_sell_date(self):
        items = [Item("Normal Item", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(8, items[0].quality)
    def test_normal_item_sell_in_decreases(self):
        items = [Item("smth", 2, -1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(1, items[0].sell_in)

    def test_normal_item_quality_never_negative(self):
        items = [Item("smth", -1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_expired_normal_item_quality_decreases_twice_as_fast(self):
        items = [Item("smth", -1, 2)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_aged_brie_quality_increases(self):
        items = [Item("Aged Brie", 2, 40)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(41, items[0].quality)

    def test_aged_brie_quality_never_exceeds_50(self):
        items = [Item("Aged Brie", 2, 60)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(60, items[0].quality)

    def test_expired_aged_brie_quality_increases_twice_as_fast(self):
        items = [Item("Aged Brie", -1, 40)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(42, items[0].quality)

    def test_expired_aged_brie_quality_still_capped_at_50_after_expiration(self):
        items = [Item("Aged Brie", -1, 60)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(60, items[0].quality)

    def test_backstage_pass_quality_increases_normal(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 12, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(31, items[0].quality)

    def test_backstage_pass_at_max_quality_does_not_increase(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
    def test_backstage_pass_quality_increases_by_2_when_10_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 7, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(32, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_when_5_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 3, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(33, items[0].quality)

    def test_backstage_pass_quality_drops_to_zero_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", -1, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_sulfuras_never_changes_quality_or_sell_in(self):
        items = [Item("Sulfuras, Hand of Ragnaros", -3, 30)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(-3, items[0].sell_in)
        self.assertEqual(30, items[0].quality)

    def test_item_string_representation(self):
        items = [Item("smth", -1, 1)]
        self.assertEqual("smth, -1, 1", items[0].__repr__())

    def test_multiple_items_update_correctly(self):
        items = [
            Item("+5 Dexterity Vest", 10, 20),#normal item
            Item("Aged Brie", 2, 0),#aged brie -> increases in quality
            Item("Elixir of the Mongoose", 5, 7),#normal item 2
            Item("Sulfuras, Hand of Ragnaros", 0, 80),#sulfuras never changes
            Item("Backstage passes to a TAFKAL80ETC concert", 15, 20),#backstage passes -> increases in quality
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 20),#backstage passes -> increases in quality a lot when concert is close
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(19, items[0].quality)
        self.assertEqual(1, items[1].quality)
        self.assertEqual(6, items[2].quality)
        self.assertEqual(80, items[3].quality)
        self.assertEqual(21, items[4].quality)
        self.assertEqual(23, items[5].quality)


        
if __name__ == '__main__':
    unittest.main()
