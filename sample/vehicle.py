# clamming.sample.vehicle.py
#
# This file is part of ClammingPy tool.
# (C) 2023-2025 Brigitte Bigi, CNRS,
# Laboratoire Parole et Langage, Aix-en-Provence, France.
#
# Use of this software is governed by the GNU Public License, version 3.
#
# ClammingPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ClammingPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ClammingPy. If not, see <http://www.gnu.org/licenses/>.
#
# This banner notice must not be removed.
# ---------------------------------------------------------------------------


import unittest

# ---------------------------------------------------------------------------


class Vehicle:
    """Represent data of a vehicle, used to illustrate `clamming` tool.

    :Author: Brigitte Bigi
    :Contact: contact@sppas.org
    :Version: 1.2 of 2024/01/06
    :License: GNU GPL version 3
    :Copyright: (C) 2023-2025 Brigitte Bigi, CNRS, Laboratoire Parole et Langage, Aix-en-Provence, France

    ### Overview

    Vehicle is a Python sample class which can be converted to markdown
    or to HTML. Its purpose is to illustrate the `clamming` features.

    :example:
    >>># Create my vehicle
    >>>my_vehicle = Vehicle("Solex", "3800", "1968")
    >>># Indicate two new drove distances
    >>>my_vehicle.dist_up(30.)
    >>>my_vehicle.dist_up(21.)
    >>># Ask for the total drove distance
    >>>my_vehicle.dist
    >>>51.
    >>># Print all known information
    >>>print(my_vehicle)
    >>>"The vehicle Solex-3800 manufactured in 1968 drove a total of 51.0 kilometers."

    ### Other information

    markdown2 library is used to convert docstrings into HTML.

    """

    def __init__(self, brand: str, model: str, year: int):
        """Create a new vehicle 🚗.

        :param brand: (str) The brand of the vehicle.
        :param model: (str) The model of the vehicle.
        :param year: (int) Year of the manufacture.

        :raises: TypeError: if invalid parameter type
        :raise: ValueError: if invalid year value

        """
        self.__brand = str(brand)
        self.__model = str(model)
        self.__check_year(year)
        self.__year = year
        self.__dist = 0.

    # an example of un-documented function
    def __check_year(self, year):
        try:
            year = int(year)
        except:
            raise TypeError("Year should be an integer.")
        if year < 1890:
            raise ValueError("Manufacture of a vehicle is certainly not before 1890!")
        if year > 2023:
            raise ValueError("Manufacture of a vehicle is supposed to be done...")

    @property
    def brand(self) -> str:
        """Get the brand of the vehicle.

        :return: (str) Brand name
        
        """
        return self.__brand

    @property
    def model(self) -> str:
        """Get the model of the vehicle.

        :returns: (str) Model name

        """
        return self.__model

    @property
    def year(self) -> int:
        """Get the year of the vehicle.

        :return:
            (int) Year name

        """
        return self.__year

    def get_dist(self) -> float:
        """Get the total dist the vehicle drove.

        :return: (float) Distance.
        The distance value does not care about the unit: km/h, mph...

        """
        return self.__dist

    def set_dist(self, value: float) -> None:
        """Set the total dist the vehicle drove.

        :param value: (float) Distance

        """
        try:
            value = float(value)
        except:
            raise TypeError("Expected a float for distance value.")
        if value < 0.:
            raise ValueError("A vehicle can't drive a negative distance...")
        self.__dist = value

    dist = property(get_dist, set_dist)

    def dist_up(self, value: float) -> float:
        """Add a new drive distance.

        :param value: (float) new distance to take into account. This value is
            added to the stored one.

        :example:
        >>> car = Vehicle("Brand", "Model", 1950)
        >>> car.dist_up(12.)
        >>> total_drive = car.dist_up(32)
        >>> print(total_drive)
        >>> 44.

        :return: (float) Total drive distance with the vehicle
        :raises: ValueError if negative value

        """
        value = float(value)
        if value < 0.:
            raise ValueError("A distance is certainly not negative... even when driving backwards!")
        if value > 0.:
            self.__dist += value
        return self.__dist

    def __str__(self):
        """Define the output string when writing the class."""
        return "The vehicle {brand}-{model} manufactured in {year} drove a " \
               "total of {dist} kilometers."\
               "".format(brand=self.__brand, model=self.__model,
                         year=self.__year, dist=self.__dist)

# ---------------------------------------------------------------------------


class TestVehicle(unittest.TestCase):
    """Tests the Vehicle object.

    It tests initialization of the Vehicle object, the dist_up method,
    and the __str__ method. It checks for valid inputs, invalid inputs,
    and expected behavior.

    Run this unittest by executing the script.

    """

    def test_init(self):
        my_vehicle = Vehicle("Solex", "3800", 1968)
        self.assertEqual(my_vehicle.brand, "Solex")
        self.assertEqual(my_vehicle.model, "3800")
        self.assertEqual(my_vehicle.year, 1968)
        self.assertEqual(my_vehicle.dist, 0.)

        with self.assertRaises(ValueError):
            # Test for invalid year
            Vehicle("Solex", "3800", 1880)
            Vehicle("Solex", "3800", 3000)

        with self.assertRaises(TypeError):
            # Test for invalid parameter types
            Vehicle("Solex", "3800", "xxxx")

    def test_dist(self):
        my_vehicle = Vehicle("Solex", "3800", 1968)
        my_vehicle.set_dist(234.)
        self.assertEqual(my_vehicle.get_dist(), 234.)

        with self.assertRaises(TypeError):
            my_vehicle.set_dist("azerty")

        with self.assertRaises(ValueError):
            my_vehicle.set_dist(-234)

    def test_dist_up(self):
        my_vehicle = Vehicle("Solex", "3800", 1968)
        self.assertEqual(my_vehicle.dist_up(30), 30.0)
        self.assertEqual(my_vehicle.dist_up(50), 80.0)
        self.assertEqual(my_vehicle.dist_up(0), 80.0)

        with self.assertRaises(ValueError):
            # Test for negative distance
            my_vehicle.dist_up(-10)

    def test_str(self):
        my_vehicle = Vehicle("Solex", "3800", 1968)
        self.assertEqual(
            str(my_vehicle),
            "The vehicle Solex-3800 manufactured in 1968 drove a total of 0.0 kilometers."
        )

# ---------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()

