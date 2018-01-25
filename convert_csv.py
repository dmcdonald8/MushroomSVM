from pandas import read_csv

class Converter:

    def __init__(self):
        
        self.df = read_csv('mushroom.csv')
        
        self.cap_shape = [ "b", "c", "x", "f", "k", "s" ]
        self.cap_surface = [ "f", "g", "y", "s" ]
        self.cap_color = [ "n", "b", "c", "g", "r", "p", "u", "e", "w", "y" ]
        self.bruises = [ "t", "f" ]
        self.odor = [ "a", "l", "c", "y", "f", "m", "n", "p", "s"]
        self.gill_attachment = ["a", "d", "f", "n" ]
        self.gill_spacing = [ "c", "w", "d" ]
        self.gill_size = [ "b", "n" ]
        self.gill_color = ["k", "n", "b", "h", "g", "r", "o", "p", "u", "e",
                           "w", "y" ]
        self.stalk_shape = ["e", "t"]
        self.stalk_sar = ["f", "y", "k", "s"]
        self.stalk_sbr = ["f", "y", "k", "s"]
        self.stalk_car = ["n", "b", "c", "g", "o", "p", "e", "w", "y"]
        self.stalk_cbr = ["n", "b", "c", "g", "o", "p", "e", "w", "y"]
        self.veil_type = ["p", "u"]
        self.veil_color = ["n", "o", "w", "y"]
        self.ring_number = ["n", "o", "t"]
        self.ring_type = ["c", "e", "f", "l", "n", "p", "s", "z"]
        self.spore_print_color = ["k", "n", "b", "h", "r", "o", "u", "w", "y"]
        self.population = ["a", "c", "n", "s", "v", "y"]
        self.habitat = ["g", "l", "m", "p", "u", "w", "d"]
        self._class = ["e", "p"]
        
    def generate_numerical_csv(self):
        
        self.df['cap-shape'].replace(self.generate_dict(self.cap_shape),
               inplace=True)
        self.df['cap-surface'].replace(self.generate_dict(self.cap_surface),
               inplace=True)
        self.df['cap-color'].replace(self.generate_dict(self.cap_color),
               inplace=True)
        self.df['bruises'].replace(self.generate_dict(self.bruises),
               inplace=True)
        self.df['odor'].replace(self.generate_dict(self.odor),
               inplace=True)
        self.df['gill-attachment'].replace(self.generate_dict(self.gill_attachment),
               inplace=True)
        self.df['gill-spacing'].replace(self.generate_dict(self.gill_spacing),
               inplace=True)
        self.df['gill-size'].replace(self.generate_dict(self.gill_size),
               inplace=True)
        self.df['gill-color'].replace(self.generate_dict(self.gill_color),
               inplace=True)
        self.df['stalk-shape'].replace(self.generate_dict(self.stalk_shape),
               inplace=True)
        self.df['stalk-surface-above-ring'].replace(self.generate_dict(self.stalk_sar),
               inplace=True)
        self.df['stalk-surface-below-ring'].replace(self.generate_dict(self.stalk_sbr),
               inplace=True)
        self.df['stalk-color-above-ring'].replace(self.generate_dict(self.stalk_car),
               inplace=True)
        self.df['stalk-color-below-ring'].replace(self.generate_dict(self.stalk_car),
               inplace=True)
        self.df['veil-type'].replace(self.generate_dict(self.veil_type),
               inplace=True)
        self.df['veil-color'].replace(self.generate_dict(self.veil_color),
               inplace=True)
        self.df['ring-number'].replace(self.generate_dict(self.ring_number),
               inplace=True)
        self.df['ring-type'].replace(self.generate_dict(self.ring_type),
               inplace=True)
        self.df['spore-print-color'].replace(self.generate_dict(self.spore_print_color),
               inplace=True)
        self.df['population'].replace(self.generate_dict(self.population),
               inplace=True)
        self.df['habitat'].replace(self.generate_dict(self.habitat),
               inplace=True)
        self.df['Class'].replace(self.generate_dict(self._class),
               inplace=True)
        
        outfile = open('mushroom-numerical.csv', 'wb')
        self.df.to_csv(outfile, index=False)
        outfile.close()
        
    def generate_dict(self, lst):
        d = {}
        for x in range(len(lst)):
            d.update({lst[x] : int(x)})
        return d
