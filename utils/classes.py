class Person:
    def __init__(self, data: dict) -> None:
        self.first_name = data.get("first", None)
        self.last_name = data.get("last", None)
        self.email = data.get("email", None)
        self.prev_giftee = data.get("prev_giftee", None)
        self.wishlist = data.get("wishlist", None)
        self.notes = data.get("wishlist", None)

    def __repr__(self) -> str:
        return (
            f"Person(\nfirst_name={self.first_name}, last_name={self.last_name}, "
            f"email={self.email}, prev_giftee={self.prev_giftee}, "
            f"wishlist={self.wishlist}, notes={self.notes})"
        )

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name}, previous giftee: {self.prev_giftee}"
        )

    def __bool__(self) -> bool:
        checks = [self.first_name, self.last_name, self.email]
        return all(checks)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
