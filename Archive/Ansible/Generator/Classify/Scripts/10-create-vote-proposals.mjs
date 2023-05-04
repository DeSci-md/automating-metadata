import sdk from "./1-initialize-sdk.mjs";
import { ethers } from "ethers";

(async () => {
    try {
        const vote = await sdk.getContract("0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9", 'vote');
        const token = await sdk.getContract('0x6e4A2c27a080ae51C825e7b08D753D8851F9a455', 'token');
        const amount = 420_000;
        const description = "Should we call the rover eye the Photoreceptor, like from Star Wars, in the production DAO?";
        const executions = [
            {
                toAddress: token.getAddress(),
                nativeTokenValue: 0,
                transactionData: token.encoder.encode(
                    "mintTo", [
                        vote.getAddress(),
                        ethers.utils.parseUnits(amount.toString(), 18),
                    ]
                ),
            }
        ];
        await vote.propose(description, executions);
        console.log("✅ Successfully created proposal to mint tokens");
    } catch (error) {
        console.error("Failed to create proposal. ", error);
        process.exit(1);
    }
})();

/* Output:
👋 -> SDK Initialised by address:  0x15A4C3b42f3386Cd1A642908525469684Cac7C6d
✅ Successfully created proposal to mint tokens
*/