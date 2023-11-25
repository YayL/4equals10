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
        l_list = self.op(l_list)
        m_list = self.op(m_list)
        r_list = self.op(r_list)
        l_list_len, r_list_len = len(l_list), len(r_list)

        results = []

        if l_list_len and r_list_len:
            for left in l_list:
                for middle in m_list:
                    l_m_list = self.str_combinations(left, "(" + middle + ")")
                    for right in r_list:
                        for left_middle in l_m_list:
                            results += self.str_combinations(left_middle, right)
        elif l_list_len:
            for left in l_list:
                for middle in m_list:
                    results += self.str_combinations(left, "(" + middle + ")")
        elif r_list_len:
            for middle in m_list:
                for right in r_list:
                    results += self.str_combinations("(" + middle + ")", right)
        else:
            results += m_list

        return results

    def solve(self):
        permutations = itertools.permutations(self.numbers, 4)
        groupings = list(itertools.combinations(list(range(0, 5)), 2))
        for perm in permutations:
            if self.GROUP:
                for group in groupings:
                    left = perm[0:group[0]]
                    middle = perm[group[0]:group[1]]
                    right = perm[group[1]:]

                    results = self.calc(left, middle, right)
            else:
                results = self.calc([], perm, [])

            for expr in results:
                try:
                    val = eval(expr)
                    if val == 10:
                        self.soloutions.append(expr)
                except ZeroDivisionError:
                    continue

nums = Numbers(map(int, list(sys.argv[1])))
nums.solve()
print(nums.soloutions)
