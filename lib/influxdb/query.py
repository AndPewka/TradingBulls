class Query:
    def __init__(self, query):
        self.__query = ""
        self.__add_part(query)
        self.__required_fields = ("measurement", "range")
        self.__used_fields = []

    def __call__(self):
        self.__validate_required()
        return str(self)

    def __str__(self):
        return self.__query

    def __add_part(self, part):
        self.__query += part + "\n"

    def __validate_required(self):
        for field in self.__required_fields:
            if field not in self.__used_fields:
                raise ValueError(f"{field} must be set")

    def __validate_used(self, field):
        if field in self.__used_fields:
            raise ValueError(f"{field} already settled")
        self.__used_fields.append(field)

    def range(self, start, stop=0, unit="h"):
        self.__validate_used("range")
        self.__add_part(f"|> range(start: -{start}{unit}, stop: -{stop}{unit})")
        return self

    def measurement(self, measurement):
        self.__validate_used("measurement")
        self.__add_part(f'|> filter(fn: (r) => r["_measurement"] == "{measurement}")')
        return self

    def filter(self, **filter_args):
        self.__validate_used("filter")
        filter_string = " and ".join([f'r["{key}"] == "{value}"' for key, value in filter_args.items()])
        self.__add_part(f'|> filter(fn: (r) => {filter_string})')
        return self

    def order_by_time_desc(self):
        self.__validate_used("order_by_time_desc")
        self.__add_part(f'|> sort(columns: ["_time"], desc: true)')
        return self

    def limit(self, n):
        self.__validate_used("limit")
        self.__add_part(f'|> limit(n: {n})')
        return self

    def group_by_time(self, amount, unit="m", aggregate_function="last"):
        self.__validate_used("aggregate")
        self.__add_part(f'|> aggregateWindow(every: {amount}{unit}, fn: {aggregate_function})')
        return self

    def first(self):
        self.__validate_used("aggregate")
        self.__add_part("|> first()")
        return self

    def last(self):
        self.__validate_used("aggregate")
        self.__add_part("|> last()")
        return self

    def keep(self, *keep_fields):
        self.__validate_used("keep")
        keep_string = str(list(keep_fields)).replace("'", '"')
        self.__add_part(f"|> keep(columns: {keep_string})")
        return self
