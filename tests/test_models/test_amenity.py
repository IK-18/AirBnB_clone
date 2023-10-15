#!/usr/bin/python3
"""Defines unittests for models/amenity.py.

Unittest classes:
    TestAmenity_instantiation
    TestAmenity_save
    TestAmenity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_class_attribute(self):
        bm = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", bm.__dict__)

    def test_unique_ids(self):
        bm1 = Amenity()
        bm2 = Amenity()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_unique_created_at(self):
        bm1 = Amenity()
        sleep(0.05)
        bm2 = Amenity()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_unique_updated_at(self):
        bm1 = Amenity()
        sleep(0.05)
        bm2 = Amenity()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = Amenity()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[Amenity] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_unused(self):
        bm = Amenity(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = Amenity("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        bm = Amenity()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_multi_save(self):
        bm = Amenity()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bm.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_with_arg(self):
        bm = Amenity()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_updates_file(self):
        bm = Amenity()
        bm.save()
        bmid = "Amenity." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_keys(self):
        bm = Amenity()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bm = Amenity()
        bm.middle_name = "Betty"
        bm.my_number = 24
        self.assertEqual("Betty", bm.middle_name)
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_strs(self):
        bm = Amenity()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["id"]))
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        bm = Amenity()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        tdict = {
                'id': '123456',
                '__class__': 'Amenity',
                'created_at': dt.isoformat(),
                'updated_at': dt.isoformat(),
                }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test__to_dict_not_dict(self):
        bm = Amenity()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(self):
        bm = Amenity()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


if __name__ == "__main__":
    unittest.main()
