from lark import Lark, Transformer, v_args

grammar = """
start: signal intervals "."       -> sentence

signal: "+"                    -> plus_signal
      | "-"                    -> minus_signal

intervals: interval remaining_intervals -> intervals
remaining_intervals:          -> empty
                   | interval remaining_intervals -> remaining_intervals
interval: "[" NUMBER ";" NUMBER "]"    -> interval

%import common.NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""


class IntervalTransformer(Transformer):
    """
    Handles transformations and applies constraints to parsed intervals.

    Attributes:
        sentido (int): Indicates the current signal direction (+1 or -1).
        anterior (float): Tracks the end value of the previous interval.
        erro (bool): Flag indicating if a constraint was violated.
    """
    def __init__(self):
        self.sentido = 0
        self.anterior = float('-inf')
        self.erro = False

    @v_args(inline=True)
    def sentence(self, signal, intervals):
        """Returns the parsed intervals."""
    # !TODO return a dict with is_valid and then the struct of data
        return {"is_valid": self.erro,
                "sentido": signal["sentido"],
                "intervalos" : intervals["intervalos"],
               "maiorAmplitude": intervals["intervalo/s_maior_amplitude"]
               }

    @v_args(inline=True)
    def plus_signal(self):
        """Sets the signal direction to +1 (growing)."""
        self.sentido = 1
        print("Signal set to + (growing).")
        return {"sentido": 1}

    @v_args(inline=True)
    def minus_signal(self):
        """Sets the signal direction to -1 (decreasing)."""
        self.sentido = -1
        self.anterior = float('inf')
        print("Signal set to - (decreasing).")
        return {"sentido": -1}

    @v_args(inline=True)
    def intervals(self, first, remaining):
        """
        Retorna a lista de intervalos processados.
        """

        dic_Intervals = [first] + remaining
        maior_Amplitude = 0
        intervals_maiorAmplitude = []
        for interval in dic_Intervals:
            amplitude = interval["end"] - interval["start"] 
            if (amplitude >= maior_Amplitude and self.sentido == +1) or (- amplitude >= maior_Amplitude and self.sentido == -1):
                
                if (self.sentido == +1):
                    maior_Amplitude = amplitude
                else: 
                    maior_Amplitude = -amplitude
                intervals_maiorAmplitude.append((interval["start"], interval["end"]))
        return {"intervalos": [first] + remaining, "intervalo/s_maior_amplitude": intervals_maiorAmplitude}
    
    
    @v_args(inline=True)
    def interval(self, start, end):
        """
        Processes an interval and checks constraints based on signal direction.
        !TODO Add a function for the remaining intervals
        """
        start = int(start)
        end = int(end)

        if self.sentido == 1:
            if end <= start:
                print(f"Error: Constraint CC1 violated. End ({end}) must be greater than Start ({start}).")
                self.erro = True
                return {"start": start, "end": end, "erro": True}
            if start < self.anterior:
                print(f"Error: Constraint CC2 violated. Start ({start}) must be greater than or equal to the previous End ({self.anterior}).")
                self.erro = True
                return {"start": start, "end": end, "erro": True}
        elif self.sentido == -1:
            if end >= start:
                print(f"Error: Constraint CC1 violated. End ({end}) must be less than Start ({start}).")
                self.erro = True
                return {"start": start, "end": end, "erro": True}
            if start > self.anterior:
                print(f"Error: Constraint CC2 violated. Start ({start}) must be less than or equal to the previous End ({self.anterior}).")
                self.erro = True
                return {"start": start, "end": end, "erro": True}

        self.anterior = end
        return {"start": start, "end": end}
    
    # passar para o interls a lista de intervalos
    @v_args(inline=True)
    def remaining_intervals(self, interval=None, rest=None):
        """
        Retorna a lista de intervalos restantes corretamente estruturada.
        """

        if interval is None: 
            return []
        if rest is None:  # Se não há mais nada, retorna apenas o intervalo
            return [interval]
        return [interval] + rest


    def empty(self, _):
        """Represents an empty remaining interval."""
        return []

parser = Lark(grammar, parser='lalr', transformer=None)

def parse_input(input_text):
    """
    Parses the input text, applies transformations, and checks constraints.

    Args:
        input_text (str): The input string to parse.

    Returns:
        None
    """
    try:
        tree = parser.parse(input_text)
        transformer = IntervalTransformer()
        result = transformer.transform(tree)
        if transformer.erro:
            print("\nParsing failed: One or more constraints were violated.")
        else:
            print("\nParsing successful: All constraints satisfied.")
            print("Parsed intervals:", result)
    except Exception as e:
        print(f"\nParsing error: {e}")

if __name__ == "__main__":
    input_text = "- [4;2] [1;0] ."
    print("Input:", input_text)
    parse_input(input_text)


