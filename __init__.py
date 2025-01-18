class MinDF:
    def __init__(self, **kwargs):
        # Verify all vectors have the same length
        lengths = {len(v) for v in kwargs.values()}
        if len(lengths) > 1:
            raise ValueError("All vectors must have the same length")
        
        self.data = kwargs
        self._length = lengths.pop() if lengths else 0
    
    def __len__(self):
        return self._length
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.data[key]
        elif isinstance(key, int):
            return {col: values[key] for col, values in self.data.items()}
        raise TypeError(f"Invalid key type: {type(key)}")
    
    def to_csv(self, filename):
        """Write the data frame to a CSV file."""
        if not self.data:
            return
        
        with open(filename, 'w') as f:
            # Write header
            f.write(','.join(self.data.keys()) + '\n')
            
            # Write rows
            for i in range(len(self)):
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
        name=['Alice', 'Bob', 'Charlie'],
        age=[25, 30, 35],
        score=[92.5, 88.0, 95.5]
    )
    
    # Save to CSV
    df.to_csv('data.csv')
    
    # Read from CSV
    df2 = MinDF.from_csv('data.csv')
    
    # Access data
    print("Names:", df['name'])
    print("First row:", df[0])