class Pressure:

    def __init__(self, condition, condition_inputs, function, function_inputs, function_constant, description):
        self.condition = condition
        self.condition_inputs = condition_inputs
        self.function = function
        self.function_inputs = function_inputs
        self.function_constant = function_constant
        self.description = description

    def is_active(self, **kwargs):
        inputs = [kwargs[_input] for _input in self.condition_inputs]
        return self.condition(*inputs)

    def __repr__(self):
        return '<Pressure-description:\'{}\'>'.format(self.description)

def pressure_tests():
    pass
if __name__ == '__main__':
    pressure_tests()
