class TableAccessAnalyzer:
    def __init__(self):
        self.table_key_write = {}   # table_name -> list of (key, pc)
        self.table_index_read = {}  # table_name -> list of (index, pc)
        self.key_index_equiv = {}   # table_name -> set of (key, index) that are equivalent

    def record_key_write(self, table_name, key, pc):
        self.table_key_write.setdefault(table_name, []).append((key, pc))

    def record_index_read(self, table_name, index, pc):
        self.table_index_read.setdefault(table_name, []).append((index, pc))

    def analyze_equivalence(self):
        for table in self.table_key_write:
            key_accesses = self.table_key_write.get(table, [])
            index_accesses = self.table_index_read.get(table, [])

            for key, key_pc in key_accesses:
                for index, index_pc in index_accesses:
                    if index_pc < key_pc:
                        if str(index) == str(key):
                            self.key_index_equiv.setdefault(table, set()).add((key, index))

    def print_equivalence(self):
        for table, pairs in self.key_index_equiv.items():
            print(f"In table '{table}', the following key-index accesses are equivalent:")
            for key, index in pairs:
                print(f"  key='{key}' <--> index={index}")


class LuaTaintAnalyzer:
    def __init__(self):
        self.taint_vars = set()
        self.key_writes = {}     # table_name -> list of (key, pc, value)
        self.index_reads = {}    # table_name -> list of (index, pc, target_var)
        self.key_index_equiv = {}  # table_name -> set of (key, index)

    def taint_source(self, var_name):
        self.taint_vars.add(var_name)

    def record_key_write(self, table, key, pc, value_var):
        self.key_writes.setdefault(table, []).append((key, pc, value_var))
        if value_var in self.taint_vars:
            self.taint_vars.add(f"{table}['{key}']")

    def record_index_read(self, table, index, pc, target_var):
        self.index_reads.setdefault(table, []).append((index, pc, target_var))

    def analyze_key_index_equivalence(self):
        for table in self.key_writes:
            key_accesses = self.key_writes.get(table, [])
            index_accesses = self.index_reads.get(table, [])
            for key, key_pc, _ in key_accesses:
                for index, index_pc, _ in index_accesses:
                    if index_pc < key_pc and str(index) == str(key):
                        self.key_index_equiv.setdefault(table, set()).add((key, index))

    def propagate_taint(self):
        self.analyze_key_index_equivalence()

        for table, equiv_set in self.key_index_equiv.items():
            for key, index in equiv_set:
                if f"{table}['{key}']" in self.taint_vars:
                    self.taint_vars.add(f"{table}[{index}]")

        for table, reads in self.index_reads.items():
            for index, _, target_var in reads:
                if f"{table}[{index}]" in self.taint_vars:
                    self.taint_vars.add(target_var)

    def is_tainted(self, var):
        return var in self.taint_vars

    def report(self):
        print("Tainted Variables:")
        for var in sorted(self.taint_vars):
            print(f"  {var}")
