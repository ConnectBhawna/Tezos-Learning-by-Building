import smartpy as sp
class Playground(sp.Contract):
    def __init__(self):
        self.init(
            num_1 = sp.nat(4),
            num_2 = sp.int(-2),
            admin = sp.test_account("admin").address,
            time = sp.timestamp(5),
            mapping_1 = sp.map(l = {}, tkey=sp.TNat, tvalue=sp.TAddress),
            mapping_2 = sp.big_map(l = {}, tkey=sp.TNat, tvalue=sp.TAddress)
        )

    @sp.entry_point
    def change_num_values(self, params):
        # Type constraining
        sp.set_type(params, sp.TRecord(num_a = sp.TNat, num_b = sp.TInt))

        # Verification statements
        sp.verify(sp.sender == self.data.admin, "NOT AUTHORISED")
        sp.verify(sp.now > self.data.time, "INVALID TIMING")

        # Storage updates
        self.data.num_1 = params.num_a

        sp.if params.num_b > 0: 
            self.data.num_2 = params.num_b
        sp.else:
            self.data.num_2 = -1 * params.num_b

    @sp.entry_point
    def change_mappings(self, num):
        # Type constraining
        sp.set_type(num, sp.TNat)

        # Storage update
        self.data.mapping_1[num] = sp.sender
        self.data.mapping_2[num] = sp.sender
    
@sp.add_test(name="main")
def test():
    scenario = sp.test_scenario()

    # Test address
    admin = sp.test_account("admin")
    alice = sp.test_account("alice")

    # Create contract
    playground = Playground()
    scenario += playground

    # change_num_values
    scenario.h2("Playground Test 1")
    scenario += playground.change_num_values(num_a = 5, num_b = 10).run(sender = admin, now = sp.timestamp(7))
    scenario.h2("Playground Test False Transaction")
    scenario += playground.change_num_values(num_a = 5, num_b = 10).run(sender = admin, now = sp.timestamp(4), valid = False)

    scenario.h2("Playground Test with DIfferent user")
    scenario += playground.change_num_values(num_a = 3, num_b = -2).run(sender = alice, now = sp.timestamp(7), valid = False)

    #it show account address
    scenario.show(alice.address)
    scenario.show(admin.address)

    # for complete details
    scenario.show(alice)



    

