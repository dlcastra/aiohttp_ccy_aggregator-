import json

from faker import Faker

fake = Faker()


def generator():
    response = {}
    for _ in range(100_000):
        unique_key = f"{fake.word()}_{fake.word()}_{fake.word()}"
        response[unique_key] = {
            "ccy_from": "USD",
            "sale": fake.pyfloat(min_value=38, max_value=43, right_digits=3, positive=True),
            "buy": fake.pyfloat(min_value=38, max_value=43, right_digits=3, positive=True)
        }

    return response


if __name__ == "__main__":
    generated_data = generator()

    with open("stress_test_data.json", "w") as file:
        json.dump(generated_data, file, indent=4)
