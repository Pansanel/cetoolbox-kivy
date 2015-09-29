# -*- coding: utf-8 -*-
##
##    firkin - a Python module to convert between units
##             <http://www.florian-diesch.de/software/firkin/>
##    Copyright (C) 2008 Florian Diesch <devel@florian-diesch.de>

##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##    (at your option) any later version.

##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.

##    You should have received a copy of the GNU General Public License along
##    with this program; if not, write to the Free Software Foundation, Inc.,
##    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##

"""
firkin is a python module to convert between different measurement
units.


Usage
=====

First we create an instance of L{UnitManager}:

>>> um=UnitManager()
    
Next we create two families of units. The first one ist C{liter} and
uses L{SIFamily} to automatically create units with the SI prefixes:
     
    >>> um.add(SIFamily(base='l', name='liter'))

Now our L{UnitManager} knows about fl, pl, nl, ..., Ml, Gl, Tl.

How many liters are 10000 ml?

    >>> um.convert_to_unit(1e4, 'ml', 'l')
    (Decimal("10.0000"), 'l')

Next we create a family by hand:
    
    >>> f=Family(name='f', base='gallon')
    >>> f.add('barrel', 36, 'gallon')
    >>> f.add('kilderkin', 0.5, 'barrel')
    >>> f.add('firkin', 0.5, 'kilderkin')

Now we have a family called C{f} that uses gallon as its base and knows about 
barrel, kilderkin and firkin, too.

How much gallons is one firkin?

    >>> f.convert(1, 'firkin', 'gallon')
    (Decimal("9.00"), 'gallon')

What's the best way to express 3 kilderkin?

    >>> f.autoconvert(3, 'kilderkin')
    (Decimal("1.50"), 'barrel')

To convert between family C{f} and family C{liter} we need to add C{f} to
our L{UnitManager} and tell how much liters (base unit of family C{liter}) a
gallon (base unit of family C{f}) is:

    >>> um.add(f, other='liter',  factor=4.54609)

Of course the L{UnitManager} can convert firkin to gallon, too:

    >>> um.convert_to_unit(1, 'firkin', 'gallon')
    (Decimal("9.00"), 'gallon')

But it also can convert firkin to liters:

    >>> um.convert_to_unit(1, 'firkin', 'l')
    (Decimal("40.9148100"), 'l')

Or find the best way to express one liter in one of the units from
family C{f}:

   >>> um.convert_to_family(1, 'l', 'f')
   (Decimal("0.219969248299"), 'gallon')

That works with barrels, too:

   >>> um.convert_to_family(1, 'barrel', 'f')
   (Decimal("1.00"), 'barrel')

A classical example: How to convert between °C and °F?

We need a family for °C:

    >>> um.add(Family(base='°C'))

and for °F.

°F  is (°C-32)/1.8:

    >>> um.add(Family(base='°F'), other='°C', offset=(-32/1.8), factor=5.0/9)

Now we can convert:

    >>> um.convert_to_unit(32, '°F', '°C')
    (Decimal("-8E-12"), '°C')
    >>> um.convert_to_unit(100, '°C', '°F')
    (Decimal("212.0"), '°F')

Converting between °C and ml isn't useful:

    >>> um.convert_to_unit(1, '°C', 'ml')
    (None, None)

@warning: firkin is alpha software. So far it seems to work for me but it may
have severe bugs I didn't noticed yet. Use it at your own risk.

Firkin is still under development and the API may change in the future.



"""


from decimal import Decimal

def to_decimal(value):
    """
    Convert I{value} to decimal.Decimal

    @type value: float or anything that can be used as argument for
                 Decimal()
    """
    if isinstance(value, float):
        value=Decimal(str(value))
    elif not isinstance(value, Decimal):
        value=Decimal(value)
    return value


class Family(object):
    """
    A I{Family} is a collection of units which are derived
    from a common base unit.

    >>> f=Family(base='gallon')
    >>> f.add('barrel', 36, 'gallon')
    >>> f.add('kilderkin', 0.5, 'barrel')
    >>> f.add('firkin', 0.5, 'kilderkin')
    >>> f.convert(1, 'firkin', 'gallon')
    (Decimal("9.00"), 'gallon')
    >>> f.autoconvert(3, 'kilderkin')
    (Decimal("1.50"), 'barrel')
    """
    def __init__(self, base, name=None):
        """
        Constructor

        @param base: common base unit
        @type base: string
        @param name: name for this family. That name can be used with
                    L{UnitManager} to refer to this family.
                    If C{None} I{base} is used as name.
        @type name: string
        """
        self.base=base
        if name is None:
            name=base
        self.name=name
        self.units={base: Decimal(1)}

        
    def add(self, name, factor, other=None):
        """
        Add another unit to this family

        @param name: The unit's name
        @type name: string
        @param factor: factor to multiply I{other} to get this unit
        @type factor: anything that L{to_decimal} can use
        @param other: Unit this one is based on. If C{None} the base
                      unit is used
        @type other: string

        @raises KeyError: if I{other} isn't known
        @raises TypeError: if I{factor} has a wrong type
        """
        if other is None:
            other=self.base
        self[name]=self[other]*to_decimal(factor)
 

    def convert(self, amount, unit, dest):
        """
        Convert I{amount} of I{unit} to unit I{dest}

        @type amount: anything that L{to_decimal} can use
        @type unit: string
        @type dest: string

        @raises KeyError: if I{unit} or I{other} isn't known
        @raises TypeError: if I{amount} has a wrong type
        
        @return: a tupel (new amount, new unit)
        """
        amount=to_decimal(amount)
        return amount*self[unit]/self[dest], dest

        
    def autoconvert(self, amount, unit):
        """
        Convert I{amount} of I{unit} to the unit that fits best.

        @type amount: anything that L{to_decimal} can use
        @type unit: string

        @raises KeyError: if I{unit} isn't known
        @raises TypeError: if I{amount} has a wrong type

        @return: a tupel (new amount, new unit)

        """
        amount=to_decimal(amount)
        units=sorted(self.units, key=lambda x: self.units[x])
        for i in range(0, len(units)-1):
            amount, unit=self.convert(amount, unit, units[i])
            if amount < self[units[i+1]] / self[units[i]]:
                break
        else:
            amount, unit=self.convert(amount, unit, units[-1])
        return amount, unit
            
                
    def __contains__(self, item):
        """
        C{item in self}

        True if item is a known unit
        @type item: string
        """
        return item in self.units

    def __getitem__(self, index):
        """
        C{self[index]}

        Get the factor you need to mutiply the base unit with to get
        unit I{index}
        @type index: string

        @raise KeyError: if unit I{index} is not known
        """
        return self.units[index]

    def __setitem__(self, index, value):
        """
        C{self[index]=foo}
        
        Set I{value} as the factor you need to mutiply the base unit
        with to get unit I{index}
        @type index: string
        @type value: anything that L{to_decimal} can use
        """        
        self.units[index]=value



class SIFamily(Family):
    """
    I{Family} that uses SI prefixes:

      - I{y} (yokto) = 10e-24
      - I{z} (zepto) = 10e-21
      - I{a} (atto)  = 10e-18
      - I{f} (femto) = 10e-15 
      - I{p} (pico)  = 10e-12
      - I{n} (nano)  = 10e-9
      - I{µ} (micro) = 10e-6
      - I{m} (milli) = 10e-3
      - I{k} (kilo)  = 10e3
      - I{M} (mega)  = 10e6
      - I{G} (giga)  = 10e9
      - I{T} (tera)  = 10e12
      - I{P} (peta)  = 10e15
      - I{E} (exa)   = 10e18
      - I{Z} (zeta)  = 10e21
      - I{Y} (yotta) = 10e24

    If  I{extended} is C{True} the folowing prefixes are added:
      - I{c} (centi) = 10e-2
      - I{d} (dezi)  = 10e-1
      - I{da} (deka) = 10e1
      - I{h} (hekto) = 10e2

    For every prefix a unit is created.

      >>> fam=SIFamily('m')
      >>> fam.convert(1e8, 'mm', 'km')
      (Decimal("100.000"), 'km')
      >>> fam.autoconvert(3.65e-4, 'km')
      (Decimal("365.0000"), 'mm')

      
    """
    def __init__(self, base, name=None, extended=False):
        super(SIFamily, self).__init__(base, name)
        factor=1000.0
        for i in ('k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'):
            self.add('%s%s'%(i, base), factor)
            factor=factor*1000
        factor=1/1000.0
        for i in ('m', 'µ', 'n', 'p', 'f', 'a', 'z', 'y'):
            self.add('%s%s'%(i, base), factor)
            factor=factor/1000
        if extended:
            self.add('h%s'%base, 100)
            self.add('da%s'%base, 10)
            self.add('d%s'%base, 1/10.0)
            self.add('c%s'%base, 1/100.0)





class Item(object):
    """
    Holds an item in L{UnitManager}

    See L{UnitManager.add}
    """
    def __init__(self, family, other, factor=1.0, offset=0.0, groups=None):
        """
        I{family}=I{other}*factor+offset

        @type family: L{Family}
        @type other: L{Family}
        @type factor: anything that L{to_decimal} can use
        @type offset: anything that L{to_decimal} can use
        """
        self.family=family
        self.other=other
        self.factor=to_decimal(factor)
        self.offset=to_decimal(offset)
        if groups is None:
            self.groups = set()
        elif isinstance(groups, basestring):
             self.groups = set((groups,))
        else:
            try:
                self.groups = set(groups)
            except TypeError:
                self.groups = set((groups, ))
        


    def __repr__(self):
        if isinstance(self.other, Family):
            other=self.other.name
        else:
            other=self.other
        return '<Item %s %s %s %s>'%(self.family.name,
                                  self.factor,
                                  self.offset,
                                  other)



class UnitManager(object):
    """
    A I{UnitManager} hold a collection of L{Family} objects and allows
    to convert between their units.

    >>> um=UnitManager()
    >>> um.add(SIFamily(base='l', name='liter'))
    >>>
    >>> f=Family(name='f', base='gallon')
    >>> f.add('barrel', 36, 'gallon')
    >>> f.add('kilderkin', 0.5, 'barrel')
    >>> f.add('firkin', 0.5, 'kilderkin')
    >>> um.add(f, other='liter',  factor=4.54609)
    >>>
    >>> um.add(Family(base='°C'))
    >>> um.add(Family(base='°F'), other='°C', offset=(-32/1.8), factor=5.0/9) 
    >>> um.convert_to_unit(1e4, 'ml', 'l')
    (Decimal("10.0000"), 'l')
    >>> um.convert_to_unit(1, 'firkin', 'gallon')
    (Decimal("9.00"), 'gallon')
    >>> um.convert_to_family(1, 'firkin', 'liter')
    (Decimal("40.9148100"), 'l')
    >>> um.convert_to_family(1, 'l', 'f')
    (Decimal("0.219969248299"), 'gallon')
    >>> um.convert_to_family(1, 'barrel', 'f')
    (Decimal("1.00"), 'barrel')
    >>> um.convert_to_unit(32, '°F', '°C')
    (Decimal("-8E-12"), '\\xc2\\xb0C')
    >>> um.convert_to_unit(100, '°C', '°F')
    (Decimal("212.0"), '\\xc2\\xb0F')
    >>> um.convert_to_unit(1, '°C', 'ml')
    (None, None)
    """

    def __init__(self):
        """
        Constructor
        """
        self.units = {}
        self.families = {}
        self.items = {}
        self.groups = {}

    def add(self, family, other=None, factor=1, offset=0, groups=None):
        """
        Add another L{Family} object.

        If I{other} is not C{None} a conversion path
        
        I{family} = I{other} * I{factor} + I{offset}

        and its reverse path are added.

        @type family: L{Family}
        @type other: L{Family} or C{string} (name of an existing family)
        @type factor: anything that L{to_decimal} can use
        @type offset: anything that L{to_decimal} can use
        @type groups: C{string} or C{iterable} of C{strings}

        @raise KeyError: if I{other} is a string and there's no known
                          unit with this name

        @raise TypeError: if I{factor} or I{offset} has a wrong type
        @raise AttributeError: if I{family} has a wrong type
        """
        self.families[family.name]=family

        if other is not None and not isinstance(other, Family):
            other=self.families[other]

        if not family.name in self.items:
            self.items[family.name]=[]

        if other is not None:
            self.items[family.name].append(Item(family=family,
                                                other=other,
                                                factor=factor,
                                                offset=offset,
                                                groups=groups)
                                           )

            if other.name in self.items:
                self.items[other.name].append(Item(family=other,
                                                   other=family,
                                                   factor=1/factor,
                                                   offset=-offset/factor,
                                                   groups=groups)
                                              )
        
        for u in family.units:
            self.units[u]=family

        if groups is not None:
            if isinstance(groups, basestring):
                groups = (groups,)
            try:
                for c in groups:
                    try:
                        self.groups[c].append(family)
                    except KeyError:
                        self.groups[c] = [family]
            except TypeError:
                try:
                    self.groups[groups].append(family)
                except KeyError:
                    self.groups[groups] = [family]  


    def shortest_path(self, start, end, path=None):
        """
        Finds the shortest conversion path between I{start} and I{end}.

        @param start: family to start with
        @type start: name of a L{Family} that has been added by L{add}
        @param end: family to end with
        @type end: name of a L{Family} that has been added by L{add}

        @returns: list of L{Item}s to convert I{start} to I{end} or
                  C{None} if no such path can be found
        """ 
        if start not in self.items or end not in self.items:
            if start in self.units:
                start=self.units[start]
            else:
                return None
        if path is None:
            path=[]
        else:
            path=[x for x in path]   # make a copy
        if start==end:
            return path
        shortest=None
        for node in self.items[start]:
            if node in path:
                continue
            newpath=self.shortest_path(node.other.name, end, path+[node])
            if newpath is not None:
                if shortest is None or len(newpath) < len(shortest):
                    shortest=newpath
        return shortest


    def convert_to_family(self, amount, unit, family):
        """
        Convert I{amount} of I{unit} to the unit in I{family} that
        fits best.

        See L{Family.autoconvert}.

        @type amount:  anything that L{to_decimal} can use
        @type unit: C{string} (name of a known unit)
        @type family: L{Family} or C{string} (name of a known family)

        @return: Tupel (new amount, new unit) or (None, None) if
                 conversion is not possible
        
        @raise KeyError: if I{unit} is not known
        @raise KeyError: if I{family} is a string an no family with
                         that name is known
        @raise TypeError: if I{amount} has a wrong type
        """
        sfam=self.units[unit]
        if isinstance(family, Family):
            dfam=family
        else:
            dfam=self.families[family]

        amount, unit=sfam.convert(amount, unit, sfam.base)

        path=self.shortest_path(sfam.name, dfam.name)
        if path is None:
            return None, None
        elif len(path)==0:
            return sfam.autoconvert(amount, unit)
        else:
            for p in path:
                amount=amount*p.factor+p.offset
            return dfam.autoconvert(amount, dfam.base)

        
    def convert_to_unit(self, amount, unit, dest):
        """
        Convert I{amount} of I{unit} to unit I{dest}.
        
        See L{Family.convert}.

        @type amount:  anything that L{to_decimal} can use
        @type unit: C{string} (name of a known unit)
        @type dest: C{string} (name of a known unit) 

        @return: Tupel (new amount, new unit) or (None, None) if conversion
                 is not possible.

        @raise KeyError: if I{unit} or I{dest} is not known
        @raise TypeError: if I{amount} has a wrong type
        """

        sfam=self.units[unit]
        dfam=self.units[dest]

        amount, unit=sfam.convert(amount, unit, sfam.base)

        path=self.shortest_path(sfam.name, dfam.name)
        if path is None:
            return None, None
        elif len(path)==0:
            return sfam.convert(amount, unit, dest)
        else:
            for p in path:
                amount=amount*p.factor+p.offset
            return dfam.convert(amount, dfam.base, dest)
        
        

    def convert_to_group(self, amount, unit, group):
        """
        Convert I{amount} of I{unit} to the unit in I{group} that
        fits best.

        See L{convert_to_family}.

        @type amount:  anything that L{to_decimal} can use
        @type unit: C{string} (name of a known unit)
        @type group: C{string} (name of a known group)

        @return: Tupel (new amount, new unit) or (None, None) if
                 conversion is not possible
        
        @raise KeyError: if I{unit} is not known
        @raise KeyError: if I{group} is not known
        @raise TypeError: if I{amount} has a wrong type
        """
        _amount = _unit = None
        for fam in self.families.values():
            if fam in self.groups[group]:
                a, u = self.convert_to_family(amount, unit, fam)
                if a is not None:
                    if ((_amount is None) or
                        (abs(a) >= 1 and abs(1-_amount) > abs(1-a)) or
                        (abs(a) < 1 and abs(1-_amount) < abs(1-a))
                        ):
                        _amount, _unit = a, u
        return _amount, _unit
                    
