import smartpy as sp

class TezosDevHub(sp.Contract):
    def __init__(self, metadata):
        self.init(
            all_devs = sp.nat(0),
            devs = sp.map(),
            metadata = metadata
        )
    
    @sp.entry_point
    def register(self, params):
        self.data.devs[self.data.all_devs] = sp.record(
            name = params.name,
            bio = params.bio,
            address = sp.sender
        )
        self.data.all_devs += 1

if "templates" not in __name__:
    @sp.add_test(name = "StoreValue")
    def test():
        # create test users
        alice = sp.test_account("alice")
        bob = sp.test_account("bob")

        # create scenario
        scenario = sp.test_scenario()

        # Add heading
        scenario.h1("Tezos Developers Hub")

        # Add subheading
        scenario.h2("Initialise the contract")
        c1 = TezosDevHub(
            metadata = sp.utils.metadata_of_url("ipfs://QmTLTbo1a9pvFf2nPNKoLUNjokyw4An9PSVkx82QzKDCtj")
        )

        # Add c1 to scenario
        scenario += c1
        
        scenario.h2("Register a user")
        # Call register entry point
        c1.register(
            name = "test name",
            bio = "Heyy there!"
        ).run(sender = alice)

        scenario.h2("Register another user")
        c1.register(
            name = "another user",
            bio = "Hii I'm new to Tezos"
        ).run(sender = bob)