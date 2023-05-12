import sdk from './1-initialize-sdk.mjs';
import { MaxUint256 } from "@ethersproject/constants";

(async () => {
    try {
        const editionDrop = await sdk.getContract("0x93FC4ba29c41c059fB9f4727F3903df776771Af8", 'edition-drop');
        const claimConditions = [{
            startTime: new Date(),
            maxClaimable: 50_000,
            price: 0,
            maxClaimablePerWallet: 1,
            waitInSeconds: MaxUint256,
        }]

        await editionDrop.claimConditions.set("0", claimConditions);
        console.log("✅ ↣ Successfully set claim conditions.");
    } catch (error) {
        console.error("Failed to get claim condition. Error: ", error);
    }
})();