import { AddressZero } from "@ethersproject/constants"
import sdk from './1-initialize-sdk.mjs'
import { readFileSync } from 'fs';

(async () => {
    try {
        const editionDropAddress = await sdk.deployer.deployEditionDrop({
            name: "Star Sailors Contributor Membership",
            description: "A Dao for early contributors to the game Star Sailors, being developed by Signal Kinetics",
            image: readFileSync("assets/ContributorCard.png"),
            primary_sale_recipient: AddressZero,
        });

        const editionDrop = await sdk.getContract(editionDropAddress, "edition-drop"); // Initialise contract through thirdweb
        const metadata = await editionDrop.metadata.get(); // Get metadata of the contract
        console.log("✅ Successfully deployed editionDrop contract, address:",
        editionDropAddress,);
        console.log("✅ editionDrop metadata:", metadata);
    } catch (error) {
        console.log("Failed to deploy editionDrop contract: ", error);
    }
})();

/* Output: 
👋 -> SDK Initialised by address:  0x15A4C3b42f3386Cd1A642908525469684Cac7C6d
✅ Successfully deployed editionDrop contract, address: 0x93FC4ba29c41c059fB9f4727F3903df776771Af8
✅ editionDrop metadata: {
  name: 'Star Sailors Contributor Membership',
  description: 'A Dao for early contributors to the game Star Sailors, being developed by Signal Kinetics',
  image: 'https://gateway.ipfscdn.io/ipfs/QmWumgB3dtWbfZmLQ2qWJkEk6nh5yXhYd4kHGt7kYtvriY/0',
  seller_fee_basis_points: 0,
  fee_recipient: '0x0000000000000000000000000000000000000000',
  merkle: {},
  symbol: ''
}
*/