# Function to get watermark weight
def get_watermark_weight():
    while True:
        try:
            weight = float(input("Enter the watermark weight (it must be a rational number between 0 and 1, excluding 0 and 1): "))
            if 0 < weight < 1:
                return weight
            else:
                print("The weight must be between 0 and 1 (exclusive).")
        except ValueError:
            print("Please enter a valid number.")