def convert_weight(w):
    if "lbs" in w:
        number = float(w.split(" ")[0])
        converted_number = round(number * 0.453592, 2)
        return f"{converted_number} kg"
    elif "kg" in w:
        number = float(w.split(" ")[0])
        rounded_number = round(number, 2)
        return f"{rounded_number} kg"
    else:
        return w


print(convert_weight('24kg,lbs'))