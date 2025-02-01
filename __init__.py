class MinDF:
    def __init__(self, **kwargs):
        # Verify all items have the same length
        if not kwargs:
            self.data = {}
            self._length = 0
            return

        # Get the length of the first item (and its key)
        first_key = next(iter(kwargs.keys()))
        expected_length = len(kwargs[first_key])

        # Check all other items -- the length must be
        # the same for all of them
        for key, item in kwargs.items():
            if len(item) != expected_length:
                raise ValueError(
                    f"Length mismatch -- '{first_key}' has length {expected_length}, "
                    f"but '{key}' has length {len(item)}"
                )

        lengths = {len(v) for v in kwargs.values()}

        self.data = kwargs
        self._length = lengths.pop() if lengths else 0
    
    def __len__(self):
        raise TypeError(
            "can't use len() with a MinDF object.\n" +
                "Use one of these instead:\n" +
                "   df.count_rows()\n" +
                "   df.count_cols()"
        )
    
    def count_rows(self):
        return self._length
    
    def count_cols(self):
        return len(self.data)
    
    def keys(self):
        return self.data.keys()
    
    def col(self, colname):
        if colname not in self.data.keys():
            raise ValueError(f"'{colname}' is not a column name")
        return self.data.get(colname)
    
    def row(self, index):
        if abs(index) >= self._length:
            raise ValueError(f"index {index} is out of range; number of rows is {self._length}")
        return {col: values[index] for col, values in self.data.items()}
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.data[key]
        elif isinstance(key, int):
            return self.row(key)
            # return {col: values[key] for col, values in self.data.items()}
        raise TypeError(f"Invalid key type: {type(key)}")
    
    # Start of internal helpers for __str__():
    def _get_column_widths(self):
        """Calculate the maximum width needed for each column."""
        widths = {}
        for col, values in self.data.items():
            # Width of column name
            max_width = len(str(col))
            # Width of longest value
            for val in values:
                max_width = max(max_width, len(str(val)))
            widths[col] = max_width
        return widths
    
    def _format_row(self, values, widths):
        """Format a single row of data with proper padding."""
        return "│ " + " │ ".join(
            str(val).ljust(widths[col]) 
            for col, val in zip(self.data.keys(), values)
        ) + " │"
    
    def _format_header(self, widths):
        """Format the header row with column names."""
        return "│ " + " │ ".join(
            col.ljust(widths[col]) 
            for col in self.data.keys()
        ) + " │"
    
    def _format_separator(self, widths, char="─"):
        """Create a separator line."""
        parts = []
        for col in self.data.keys():
            parts.append(char * widths[col])
        return f"├─{'─┼─'.join(parts)}─┤"
    
    def _format_top_border(self, widths):
        """Create the top border."""
        parts = []
        for col in self.data.keys():
            parts.append("─" * widths[col])
        return f"┌─{'─┬─'.join(parts)}─┐"
    
    def _format_bottom_border(self, widths):
        """Create the bottom border."""
        parts = []
        for col in self.data.keys():
            parts.append("─" * widths[col])
        return f"└─{'─┴─'.join(parts)}─┘"

    # Tabular string display
    def __str__(self):
        if not self.data:
            return "Empty MinDF"
        
        # Get maximum width for each column
        widths = self._get_column_widths()
        
        # Build the string representation
        lines = []
        
        # Add top border, header, and separator
        lines.append(self._format_top_border(widths))
        lines.append(self._format_header(widths))
        lines.append(self._format_separator(widths))
        
        # Add data rows
        for i in range(self.count_rows()):
            values = [self.data[col][i] for col in self.data.keys()]
            lines.append(self._format_row(values, widths))
        
        # Add bottom border
        lines.append(self._format_bottom_border(widths))
        
        return "\n".join(lines)
    
    def __repr__(self):
        if not self.data:
            return "MinDF()"
        
        # Format each column's data
        parts = []
        for col, values in self.data.items():
            parts.append(f"{col}={repr(values)}")
        
        return f"MinDF({', '.join(parts)})"

    def to_csv(self, filename):
        """Write the data frame to a CSV file."""
        if not self.data:
            return
        
        with open(filename, 'w') as f:
            # Write header
            f.write(','.join(self.data.keys()) + '\n')
            
            # Write rows
            for i in range(self.count_rows()):
                row = [str(self.data[col][i]) for col in self.data.keys()]
                f.write(','.join(row) + '\n')

        
    @classmethod
    def from_csv(cls, filename):
        """Read a CSV file into a MinDF."""
        with open(filename, 'r') as f:
            # Read header
            header = next(f).strip().split(',')
            
            # Initialize columns
            columns = {col: [] for col in header}
            
            # Read data
            for line in f:
                values = line.strip().split(',')
                for col, val in zip(header, values):
                    # Try to convert to numeric if possible
                    try:
                        val = float(val)
                        if val.is_integer():
                            val = int(val)
                    except ValueError:
                        pass
                    columns[col].append(val)
        
        return cls(**columns)

# Example usage:
if __name__ == "__main__":
    # Create a data frame
    df = MinDF(
        name=['Alice', 'Bob', 'Charlie', 'David'],
        age=[25, 30, 35, 42],
        score=[92.5, 88.0, 95.5, 65.0]
    )

    print(dict(df))
    print(f"Using .col(\"age\"): {df.col("age")}")
    index = 1
    print(f"Using .row({index}): {df.row(index)}")
    print(f"Using [{index}]: {df[index]}")

    keys_from_dict = dict(df).keys()
    print(keys_from_dict)
    
    for key in keys_from_dict:
        print(key)

    # print(f"Length of 'df': {len(df)}")
    print(f"Keys: {df.keys()}")

    print(f"Number of columns: {df.count_cols()}")
    print(f"Number of rows   : {df.count_rows()}")

    key = "name"
    print(f"Using df[\"{key}\"]: {df[key]}")
    print(f"Using df[\"age\"]: {df["age"]}")

    print("Now, the for loop:")

    for index, item in df.data.items():
        print(f"{index}: {item}")
    
    print(df.data)
        
    # Save to CSV
    df.to_csv('data.csv')
    
    # Read from CSV
    df2 = MinDF.from_csv('data.csv')
    
    # Access data
    print("Names:", df['name'])
    print("First row:", df[0])

    print(df)

    print("\nRepr:")
    print(repr(df))