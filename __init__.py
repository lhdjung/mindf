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
            """
            To avoid confusion, len() is not implemented for class MinDF.
            Use one of these instead:
            df.count_rows()
            df.count_columns()
            """
        )
    
    def count_rows(self):
        return self._length
    
    def count_columns(self):
        return len(self.data)
    
    def keys(self):
        return self.data.keys()
    
    def col(self, colname):
        if colname not in self.data.keys():
            raise ValueError(f"not a column name: '{colname}'")
        return self.data.get(colname)
    
    def row(self, index):
        if abs(index) > self._length:
            raise ValueError(f"index {index} is out of range; number of rows is {self._length}")
        return {col: values[index] for col, values in self.data.items()}
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.data[key]
        elif isinstance(key, int):
            return self.row(key)
            # return {col: values[key] for col, values in self.data.items()}
        raise TypeError(f"Invalid key type: {type(key)}")
    
    def to_csv(self, filename):
        """Write the data frame to a CSV file."""
        if not self.data:
            return
        
        with open(filename, 'w') as f:
            # Write header
            f.write(','.join(self.data.keys()) + '\n')
            
            # Write rows
            for i in range(self._length):
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
    print(f"Using .row(-2): {df.row(-2)}")

    keys_from_dict = dict(df).keys()
    print(keys_from_dict)
    
    for key in keys_from_dict:
        print(key)

    # print(f"Length of 'df': {len(df)}")
    print(f"Keys: {df.keys()}")

    print(f"Number of columns: {df.count_columns()}")
    print(f"Number of rows   : {df.count_rows()}")

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