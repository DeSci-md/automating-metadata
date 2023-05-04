import { AddressZero } from "@ethersproject/constants";
import sdk from './1-initialize-sdk.mjs';

(async () => {
    try {
        const tokenAddress = await sdk.deployer.deployToken({
            name: "Star Sailors Governance Token",
            symbol: "SAILOR",
            primary_sale_recipient: AddressZero,
        });
        console.log("✅ Successfully deployed token contract. Address: ", tokenAddress,);
    } catch (error) {
        console.error("Failed to deploy token contract. Error: ", error);
    }
})();

/* Output
👋 -> SDK Initialised by address:  0x15A4C3b42f3386Cd1A642908525469684Cac7C6d
✅ Successfully deployed token contract. Address:  0x6e4A2c27a080ae51C825e7b08D753D8851F9a455
*/