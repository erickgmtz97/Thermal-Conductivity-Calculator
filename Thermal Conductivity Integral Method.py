import math
import numpy as np

LENGTH_BETWEEN_THERMOMETERS = 50
LENGTH_TO_THERMO_1 = 20
LENGTH_TO_THERMO_2 = 70

COEFFICIENT = 7.5
EXPONENT = 1.2715


class Rod:

    def __init__(self, manufacturer, inner_diameter, outer_diameter, length):
        self.MANUFACTURER = manufacturer
        self.INNER_DIAMETER = inner_diameter
        self.OUTER_DIAMETER = outer_diameter
        self.LENGTH = length

    def getName(self):
        return self.MANUFACTURER

    def getCrossSection(self):
        return math.pi * (self.OUTER_DIAMETER ** 2 - self.INNER_DIAMETER ** 2)
    
    def getLength(self):
        return self.LENGTH


class ThermalConductivityCalculator:

    def __init__(self, warm_temperature, bath_temperature, number_rods, resistance, cross_section, length):
        self.WARM_TEMPERATURE = warm_temperature
        self.BATH_TEMPERATURE = bath_temperature
        self.NUMBER_RODS = number_rods
        self.RESISTANCE = resistance
        self.CROSS_SECTION = cross_section
        self.LENGTH = length

    def calPower(self):
        return (self.NUMBER_RODS * self.CROSS_SECTION / self.LENGTH) * COEFFICIENT / (EXPONENT + 1) * (self.WARM_TEMPERATURE ** (EXPONENT + 1) - self.BATH_TEMPERATURE ** (EXPONENT +1))

    def calCurrent(self,power):
        return (power / self.RESISTANCE) ** (1/2)

    def calVoltage(self,current):
        return current * self.RESISTANCE

    def extrapolateTempAtThermo(self, power):
        return ((self.LENGTH / self.NUMBER_RODS / self.CROSS_SECTION) * (EXPONENT + 1) / COEFFICIENT * power + self.BATH_TEMPERATURE ** (EXPONENT + 1)) ** (1 / (EXPONENT + 1))


def main():
    
    bath_temperature = []
    warm_temperature = []
    with open('bath_temperatures.txt') as file:
        for line in file:
            bath_temperature.append(float(line.split()[0]) / 1000)
            warm_temperature.append(float(line.split()[1]) / 1000)

    bath_temperature = np.array(bath_temperature)
    warm_temperature = np.array(warm_temperature)

    rod = Rod('Clear Water', 0.25 * 25.4, 0.32 * 25.4, 50)
    cal = ThermalConductivityCalculator(warm_temperature, bath_temperature, 10, 500, rod.getCrossSection(), rod.getLength())


if __name__ == '__main__':
    main()