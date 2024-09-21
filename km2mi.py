'''
Converts kilometers to miles depending on user inputs
'''

# Taking kilometer input from the user
kilometers = float(input("Enter kilometer value"))

# Conversion factor
conv_fac = 0.621371

# Calculate miles
miles = kilometers * conv_fac
print('%0.2f kilometers is equal to %0.2f miles' % (kilometers, miles))
