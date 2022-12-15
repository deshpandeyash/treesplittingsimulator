from decimal import Decimal as dc

class DeciComplex(object):
    """
    Uses the Decimal class to make a complex number
    """

    def __init__(self, real_p, imag_p=None):
        """
        :param real_p: float, int, complex or Decimal. Real part of the complex number
        :param imag_p: float, int, Decimal or remains none if real is a complex number. Real part of the complex number

        """

        # If the input is float or int, convert to decimal
        if isinstance(real_p, float) or isinstance(real_p, int):
            self.real = dc(real_p)
        elif isinstance(real_p, dc):
            self.real = real_p
        elif isinstance(real_p, complex):
            if imag_p is None:
                self.real = dc(real_p.real)
                self.imag = dc(real_p.imag)
            else:
                raise TypeError(F"{real_p.type} cannot be used along with {imag_p.type} to instiantate DeciComplex")
        else:
            raise TypeError(F"{real_p.type} cannot be used in the real part of a complex number")

        if isinstance(imag_p, float) or isinstance(imag_p, int):
            self.imag = dc(imag_p)
        elif isinstance(imag_p, dc):
            self.imag = dc(imag_p)
        elif imag_p is None:
            pass
        else:
            raise TypeError(F"{imag_p.type} cannot be used in the imaginary part of a complex number")

    def __str__(self):
        """
        To print it..
        """
        return F"DeciComplex Object : Real={self.real}, Imag={self.imag}"

    def __add__(self, other):
        """
        :param: other: float, int, Decimal. The second operand.
        """

        if isinstance(other, float) or isinstance(other, int) or isinstance(other, dc):
            real = self.real + dc(other)
            imag = self.imag
        elif isinstance(other, complex) or isinstance(other, DeciComplex):
            real = self.real + other.real
            imag = self.imag + other.imag
        else:
            raise TypeError(F"{other.type} not supported for addition with DeciComplex")
        return DeciComplex(real_p=real, imag_p=imag)

    def __sub__(self, other):
        """
        :param: other: float, int, Decimal. The second operand.
        """
        if isinstance(other, float) or isinstance(other, int) or isinstance(other, dc):
            real = self.real - other
            imag = self.imag
        elif isinstance(other, complex) or isinstance(other, DeciComplex):
            real = self.real - other.real
            imag = self.imag - other.imag
        else:
            raise TypeError(F"{other.type} not supported for subtraction with DeciComplex")
        return DeciComplex(real_p=real, imag_p=imag)

    def __mul__(self, other):
        """
        :param: other: float, int, Decimal. The second operand.
        """

        if isinstance(other, float) or isinstance(other, int) or isinstance(other, dc):
            real = self.real * other
            imag = self.imag * other
        elif isinstance(other, complex) or isinstance(other, DeciComplex):
            real = (self.real * other.real) - (self.imag * other.imag)
            imag = (self.real * other.imag) + (other.real * self.imag)
        else:
            raise TypeError(F"{other.type} not supported for multiplication with DeciComplex")
        return DeciComplex(real_p=real, imag_p=imag)

    def __truediv__(self, other):
        """
        :param: other: float, int, Decimal. The second operand.
        """

        if isinstance(other, float) or isinstance(other, int) or isinstance(other, dc):
            real = self.real / other
            imag = self.imag / other
        elif isinstance(other, complex) or isinstance(other, DeciComplex):
            denom = other.real ** 2 + other.imag ** 2
            real = ((self.real * other.real) + (self.imag * other.imag)) / denom
            imag = -(self.real * other.imag) + (other.real * self.imag) / denom
        else:
            raise TypeError(F"{other.type} not supported for multiplication with DeciComplex")
        return DeciComplex(real_p=real, imag_p=imag)

    def __neg__(self):
        """
        Negate the entire complex number
        """
        return DeciComplex(real_p=-self.real, imag_p=-self.imag)

    def conjugate(self):
        """
        Returns the complex Conjugate of the DeciComplex object
        """
        return DeciComplex(real_p=self.real, imag_p=-self.imag)

    def __abs__(self):
        """
        Convert to absolute
        :returns: a Decimal Object
        """

        return ((self.real * self.real) + (self.imag * self.imag)).sqrt()
