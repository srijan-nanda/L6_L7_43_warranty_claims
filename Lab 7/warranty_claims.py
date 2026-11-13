
def parse_claim(text):
    try:
        if not isinstance(text, str):
            return ("", 0.0)

        parts = text.split(":")
        if len(parts) != 2:
            return ("", 0.0)

        plan, months = parts
        return plan.strip().title(), float(months)
    except (ValueError, TypeError):
        return ("", 0.0)


def age_average(ages_csv):
    try:
        if not isinstance(ages_csv, str):
            return 0

        values = [
            int(value.strip())
            for value in ages_csv.split(",")
            if value.strip()
        ]

        if not values:
            return 0

        return sum(values) / len(values)
    except (ValueError, TypeError):
        return 0


def payable_charge(text):
    try:
        if not isinstance(text, str):
            return 0

        parts = text.split("|")
        if len(parts) != 2:
            return 0

        charge, discount = parts
        total = float(charge) * 1.18 - float(discount)

        return max(total, 0)
    except (ValueError, TypeError):
        return 0


def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
	
