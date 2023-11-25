import sys
import itertools


class Numbers:
    def __init__(self, arr):
        self.numbers = arr
        self.ADD = True
        self.MINUS = True
        self.MULT = True
        self.DIV = True
        self.GROUP = True
        self.soloutions = []

    def get_sol(self):
        return self.soloutions[0] if len(self.soloutions) else "None found"

    def str_combinations(self, left, right):
        res = []
        if (self.ADD):
            res.append(left + "+" + right)
        if (self.MINUS):
            res.append(left + "-" + right)
        if (self.MULT):
            res.append(left + "*" + right)
        if (self.DIV):
            res.append(left + "/" + right)

        return res

    def op(self, arr, string=""):
        if (len(arr) == 0):
            return []
        if (len(arr) == 1):
            return [string + str(arr[0])]

        number = arr[0]
        new_arr = arr[1:]

        res = []
        if (self.ADD):
            res += self.op(new_arr, string + str(number) + "+")
        if (self.MINUS):
            res += self.op(new_arr, string + str(number) + "-")
        if (self.MULT):
            res += self.op(new_arr, string + str(number) + "*")
        if (self.DIV):
            res += self.op(new_arr, string + str(number) + "/")

        return res

    def calc(self, l_list, m_list, r_list):
        l_list, m_list, r_list = self.op(l_list), self.op(m_list), self.op(r_list)
        l_list_len, r_list_len = len(l_list), len(r_list)

        results = []

        if not self.GROUP:
            results += m_list
        elif l_list_len and r_list_len:
            for left in l_list:
                for middle in m_list:
                    for left_middle in self.str_combinations(left, "(" + middle + ")"):
                        for right in r_list:
                            results += self.str_combinations(left_middle, right)
        elif l_list_len:
            for left in l_list:
                for middle in m_list:
                    results += self.str_combinations(left, "(" + middle + ")")
        else:
            for middle in m_list:
                for right in r_list:
                    results += self.str_combinations("(" + middle + ")", right)

        return results

    def solve(self):
        permutations = itertools.permutations(self.numbers, len(self.numbers))
        groupings = list(itertools.combinations(list(range(0, len(self.numbers) + 1)), 2))
        for perm in permutations:
            results = []
            if self.GROUP:
                results = []
                for group in groupings:
                    results += self.calc(perm[0:group[0]], perm[group[0]:group[1]], perm[group[1]:])
            else:
                results = self.calc([], perm, [])

            for expr in results:
                try:
                    val = eval(expr)
                    if val == 10:
                        self.soloutions.append(expr)
                except ZeroDivisionError:
                    continue

nums_with_group = Numbers(list(map(int, list(sys.argv[1]))))

nums_without_group = Numbers(nums_with_group.numbers)
nums_without_group.GROUP = False

nums_with_group.solve()
nums_without_group.solve()
print(f"With grouping({len(nums_with_group.soloutions)}) = {nums_with_group.get_sol()}")
print(f"Without grouping({len(nums_without_group.soloutions)}) = {nums_without_group.get_sol()}")
